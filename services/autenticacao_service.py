import logging
import os
import requests

logger = logging.getLogger(__name__)


class AutenticacaoService:

    def __init__(self, base_url: str = None):
        self.base_url = (
            base_url
            or os.getenv(
                "CONECTA_HUB_URL",
                "https://conectahub-internal.sacavalcante.com.br/api/v1/liberação-estacionamento"
            ).rstrip("/")
        )

    def autenticar(self, usuario: str, senha: str) -> dict:
        url = f"{self.base_url}/auth/login"
        payload = {"usuario": usuario, "senha": senha}

        try:
            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                dados = response.json()
                return {
                    "sucesso": True,
                    "usuario_id": dados.get("usuario_id"),
                    "usuario": dados.get("usuario"),
                    "perfil": dados.get("perfil"),
                    "token": dados.get("token")
                }

            if response.status_code in (400, 401):
                erro = response.json()
                return {
                    "sucesso": False,
                    "mensagem": erro.get("mensagem", "Usuário ou senha inválidos."),
                }

            return {
                "sucesso": False,
                "mensagem": f"Erro inesperado na API ({response.status_code})",
            }

        except requests.exceptions.RequestException as e:
            logger.error("Erro na chamada de autenticação: %s", e)
            return {
                "sucesso": False,
                "mensagem": f"Não foi possível conectar à API de autenticação: {str(e)}",
            }