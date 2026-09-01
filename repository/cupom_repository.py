import logging
import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class CupomRepository:

    def __init__(
        self,
        base_url: str | None = None,
        usuario: str | None = None,
        senha: str | None = None,
    ):
        url_env = os.getenv(
            "CONECTA_HUB_URL",
            "https://conectahub-internal.sacavalcante.com.br/api/v1/liberacao-estacionamento",
        )

        if not url_env.rstrip("/").endswith("/api/v1/liberacao-estacionamento"):
            url_env = f"{url_env.rstrip('/')}/api/v1/liberacao-estacionamento"

        self.base_url = (base_url or url_env).rstrip("/")

        user = usuario or os.getenv("CONECTA_HUB_USER", "psqladmin")
        password = senha or os.getenv("CONECTA_HUB_PASSWORD", "")

        self.auth = (user, password) if user and password else None
        self.headers = {"Content-Type": "application/json"}

    def buscar_cupom(self, cpf: str):
        cpf_limpo = re.sub(r"\D", "", str(cpf or ""))
        url = f"{self.base_url}/cupons/buscar"

        try:
            response = requests.get(
                url,
                params={"document": cpf_limpo},
                headers=self.headers,
                auth=self.auth,
                timeout=10,
            )

            if response.status_code == 404:
                logger.warning("Cupom não encontrado no ConectaHub para o documento %s", cpf_limpo)
                return None

            response.raise_for_status()
            data = response.json()

            # Log para inspecionar a estrutura exata retornada pela API
            logger.info("Resposta bruta do ConectaHub para CPF %s: %s", cpf_limpo, data)

            return self._extrair_dados(data)

        except requests.RequestException as err:
            logger.error("Erro ao buscar cupom no ConectaHub (%s): %s", url, err)
            return None

    def _extrair_dados(self, data):
        if not data:
            return None

        # Desempacota envelopes comuns da API
        if isinstance(data, dict):
            conteudo = (
                data.get("dados")
                or data.get("data")
                or data.get("cupons")
                or data.get("resultado")
            )
            if conteudo is not None:
                data = conteudo
            elif data.get("sucesso") is False:
                return None

        # Se o conteúdo extraído for uma lista de cupons
        if isinstance(data, list):
            return data[0] if len(data) > 0 else None

        # Se já for o dicionário do cupom diretamente
        if isinstance(data, dict) and len(data) > 0:
            return data

        return None