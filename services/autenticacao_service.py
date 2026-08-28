import logging
import os
import bcrypt
import requests

logger = logging.getLogger(__name__)


class AutenticacaoService:

    def __init__(self, base_url: str = None):
        self.base_url = (
            base_url
            or os.getenv(
                "CONECTA_HUB_URL",
                "https://conectahub-internal.sacavalcante.com.br/api/v1/liberacao-estacionamento",
            ).rstrip("/")
        )

    def _validar_hash(self, senha_plana: str, hash_banco: str) -> bool:
        """Compara a senha digitada com o hash Bcrypt armazenado no banco."""
        try:
            if hash_banco.startswith("$2a$") or hash_banco.startswith("$2b$"):
                return bcrypt.checkpw(
                    senha_plana.encode("utf-8"),
                    hash_banco.encode("utf-8")
                )
        except Exception as err:
            logger.error("Erro ao validar hash de senha: %s", err)

        # Fallback para comparação direta em texto puro (caso o banco não use Bcrypt)
        return senha_plana == hash_banco

    def autenticar(self, usuario: str, senha: str) -> dict:
        url = f"{self.base_url}/busca-usuario"
        usuario_limpo = usuario.strip() if usuario else ""

        # Envia SOMENTE o campo usuario para bater com o WHERE da query
        payload = {"usuario": usuario_limpo}

        try:
            logger.info("Buscando usuário '%s' em %s", usuario_limpo, url)

            # Requisicao POST passando apenas 'usuario'
            response = requests.post(url, json=payload, timeout=10)

            # Caso a API utilize GET com parâmetros de query, use a linha abaixo:
            # response = requests.get(url, params={"usuario": usuario_limpo}, timeout=10)

            logger.info("Resposta API [%s]: %s", response.status_code, response.text)

            if response.status_code == 200:
                dados = response.json()

                # Trata retorno caso a API devolva uma lista ou um objeto direto
                usuario_db = dados[0] if isinstance(dados, list) and dados else dados

                if not isinstance(usuario_db, dict) or not usuario_db.get("usuario"):
                    return {
                        "sucesso": False,
                        "mensagem": "Usuário ou senha inválidos."
                    }

                hash_banco = usuario_db.get("senha_hash") or usuario_db.get("senha")

                # Valida a senha informada no formulário contra o hash retornado
                if hash_banco and self._validar_hash(senha, hash_banco):
                    return {
                        "sucesso": True,
                        "usuario_id": usuario_db.get("id") or usuario_db.get("usuario_id"),
                        "usuario": usuario_db.get("usuario"),
                        "perfil": usuario_db.get("perfil", "OPERADOR"),
                        "token": usuario_db.get("token"),
                    }

                return {
                    "sucesso": False,
                    "mensagem": "Usuário ou senha inválidos."
                }

            return {
                "sucesso": False,
                "mensagem": "Usuário ou senha inválidos."
            }

        except requests.exceptions.RequestException as e:
            logger.error("Erro de comunicação com a API ConectaHub: %s", e)
            return {
                "sucesso": False,
                "mensagem": f"Não foi possível conectar à API de autenticação: {str(e)}"
            }