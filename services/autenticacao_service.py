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
                "https://conectahub-internal.sacavalcante.com.br/api/v1/liberacao-estacionamento",
            ).rstrip("/")
        )

    def autenticar(self, usuario: str, senha: str) -> dict:
        url = f"{self.base_url}/login"
        payload = {"usuario": usuario, "senha": senha}

        try:
            logger.info("Enviando requisição de login para %s (usuário: '%s')", url, usuario)

            response = requests.post(url, json=payload, timeout=10)

            # LOGS DE DIAGNÓSTICO: exibem exatamente o status e o corpo retornado pela API ConectaHub
            logger.info("Resposta da API ConectaHub [Status %s]: %s", response.status_code, response.text)

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
                try:
                    erro = response.json()
                except ValueError:
                    erro = {}

                # Trata respostas em padrão personalizado ou FastAPI (campo "detail")
                mensagem_erro = erro.get("mensagem")
                if not mensagem_erro and "detail" in erro:
                    detail = erro["detail"]
                    mensagem_erro = detail.get("mensagem") if isinstance(detail, dict) else str(detail)

                return {
                    "sucesso": False,
                    "mensagem": mensagem_erro or "Usuário ou senha inválidos.",
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