import logging
<<<<<<< HEAD

import bcrypt

logger = logging.getLogger(__name__)
=======
import os
import requests
>>>>>>> eda019813909102135d79eece075129c34643f43


class AutenticacaoService:

<<<<<<< HEAD
    def __init__(self):
        from conectahub_client import ConectaHubClient

        self.conectahub_client = ConectaHubClient()

    def _validar_hash(self, senha_plana: str, hash_banco: str) -> bool:
        """Compara a senha digitada no formulário com o hash Bcrypt retornado pelo banco."""
        try:
            # PIE810: Uso de tupla no startswith
            if hash_banco.startswith(("$2a$", "$2b$")):
                return bcrypt.checkpw(
                    senha_plana.encode("utf-8"), hash_banco.encode("utf-8")
                )
        except (ValueError, TypeError) as err:  # BLE001: Captura exceções específicas
            logger.error("Erro ao validar hash Bcrypt: %s", err)

        return senha_plana == hash_banco

    def autenticar(self, usuario: str, senha: str) -> dict:
        usuario_limpo = usuario.strip() if usuario else ""
        senha_limpa = senha.strip() if senha else ""

        try:
            logger.info("Buscando usuário '%s' na API ConectaHub", usuario_limpo)

            dados = self.conectahub_client.buscar_usuario(usuario=usuario_limpo)
            logger.info("Retorno da busca de usuário: %s", dados)

            usuario_db = dados[0] if isinstance(dados, list) and dados else dados

            if not isinstance(usuario_db, dict) or not usuario_db.get("usuario"):
                return {
                    "sucesso": False,
                    "mensagem": "Usuário ou senha inválidos.",
                }

            hash_banco = usuario_db.get("senha_hash") or usuario_db.get("senha")

            if hash_banco and self._validar_hash(senha_limpa, hash_banco):
                return {
                    "sucesso": True,
                    "usuario_id": usuario_db.get("id")
                    or usuario_db.get("usuario_id"),
                    "usuario": usuario_db.get("usuario"),
                    "perfil": usuario_db.get("perfil", "OPERADOR"),
                    "token": usuario_db.get("token"),
                }

            return {
                "sucesso": False,
                "mensagem": "Usuário ou senha inválidos.",
            }

        except Exception as e:  # noqa: BLE001
            logger.error("Erro na autenticação via ConectaHubClient: %s", e)
            return {
                "sucesso": False,
                "mensagem": "Serviço de autenticação temporariamente indisponível.",
            }
=======
  def __init__(self, base_url: str = None):
    self.base_url = (
        base_url
        or os.getenv(
            "CONECTA_HUB_URL",
            "https://conectahub.sacavalcante.com.br/api/v1",
        ).rstrip("/")
    )

  def autenticar(self, usuario: str, senha: str) -> dict:
    url = f"{self.base_url}/liberação-de-estacionamento/login"

    # Envia o usuário e senha no corpo da requisição POST
    payload = {"usuario": usuario, "senha": senha}

    try:
      response = requests.post(
          url, json=payload, headers={"Content-Type": "application/json"}, timeout=10
      )

      if response.status_code == 200:
        dados = response.json()
        return {
            "sucesso": True,
            "usuario_id": dados.get("usuario_id"),
            "usuario": dados.get("usuario"),
            "perfil": dados.get("perfil"),
            "token": dados.get("token"),
        }

      if response.status_code in (400, 401):
        erro = response.json()
        return {
            "sucesso": False,
            "mensagem": erro.get("mensagem", "Usuário ou senha inválidos."),
        }

      return {
          "sucesso": False,
          "mensagem": f"Erro na API de autenticação ({response.status_code}).",
      }

    except requests.exceptions.RequestException as e:
      return {
          "sucesso": False,
          "mensagem": "Falha de conexão com o servidor de autenticação.",
      }
>>>>>>> eda019813909102135d79eece075129c34643f43
