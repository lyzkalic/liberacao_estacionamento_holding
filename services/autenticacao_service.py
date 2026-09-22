import logging
import os

import bcrypt
import requests

logger = logging.getLogger(__name__)


class AutenticacaoService:
    def __init__(self, base_url: str | None = None):
        self.base_url = (
            base_url
            or os.getenv(
                "CONECTA_HUB_URL",
                "https://conectahub.sacavalcante.com.br/api/v1",
            ).rstrip("/")
        )

        try:
            from conectahub_client import ConectaHubClient
        except (ImportError, ModuleNotFoundError):  # pragma: no cover - fallback opcional
            self.conectahub_client = None
            return

        try:
            self.conectahub_client = ConectaHubClient()
        except (TypeError, ValueError):  # pragma: no cover - fallback opcional
            self.conectahub_client = None

    def _validar_hash(self, senha_plana: str, hash_banco: str) -> bool:
        """Compara a senha digitada no formulário com o hash Bcrypt do banco."""
        try:
            if hash_banco and hash_banco.startswith(("$2a$", "$2b$")):
                return bcrypt.checkpw(
                    senha_plana.encode("utf-8"), hash_banco.encode("utf-8")
                )
        except (ValueError, TypeError) as err:
            logger.error("Erro ao validar hash Bcrypt: %s", err)

        return senha_plana == hash_banco

    def autenticar(self, usuario: str, senha: str) -> dict:
        usuario_limpo = usuario.strip() if usuario else ""
        senha_limpa = senha.strip() if senha else ""

        try:
            if self.conectahub_client is not None:
                logger.info("Buscando usuário '%s' na API ConectaHub", usuario_limpo)

                dados = self.conectahub_client.buscar_usuario(usuario=usuario_limpo)
                logger.info("Retorno da busca de usuário: %s", dados)

                usuario_db = dados[0] if isinstance(dados, list) and dados else dados

                if isinstance(usuario_db, dict) and usuario_db.get("usuario"):
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

            url = f"{self.base_url}/liberação-de-estacionamento/login"
            payload = {"usuario": usuario_limpo, "senha": senha_limpa}

            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            if response.status_code == 200:
                dados = response.json()
                if isinstance(dados, dict):
                    return {
                        "sucesso": True,
                        "usuario_id": dados.get("usuario_id"),
                        "usuario": dados.get("usuario"),
                        "perfil": dados.get("perfil", "OPERADOR"),
                        "token": dados.get("token"),
                    }
                return {
                    "sucesso": False,
                    "mensagem": "Usuário ou senha inválidos.",
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
            logger.error("Erro na autenticação via API: %s", e)
            return {
                "sucesso": False,
                "mensagem": "Falha de conexão com o servidor de autenticação.",
            }
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as e:
            logger.error("Erro na autenticação via ConectaHubClient: %s", e)
            return {
                "sucesso": False,
                "mensagem": "Serviço de autenticação temporariamente indisponível.",
            }
