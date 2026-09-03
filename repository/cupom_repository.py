import logging
import os
import re

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

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
            "CONECTAHUB_URL",
            "https://conectahub-internal.sacavalcante.com.br/api/v1/liberacao-estacionamento",
        )

        if not url_env.rstrip("/").endswith("/api/v1/liberacao-estacionamento"):
            url_env = f"{url_env.rstrip('/')}/api/v1/liberacao-estacionamento"

        self.base_url = (base_url or url_env).rstrip("/")

        user = (
            usuario
            or os.getenv("CONECTAHUB_USER")
            or os.getenv("CONECTAHUB_USER")
            or "psqladmin"
        )
        password = (
            senha
            or os.getenv("CONECTAHUB_PASSWORD")
            or os.getenv("CONECTAHUB_PASSWORD")
            or ""
        )

        self.auth = (user, password) if user and password else None
        self.headers = {"Content-Type": "application/json"}

        # Configura sessão HTTP com 3 tentativas automáticas
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,  # Aguarda 1s, 2s, 4s entre tentativas
            status_forcelist=[500, 502, 503, 504],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def buscar_cupom(self, cpf: str):
        cpf_limpo = re.sub(r"\D", "", str(cpf or ""))
        url = f"{self.base_url}/buscar-cupom"

        try:
            # Timeout curto (3s para conectar, 10s para responder)
            response = self.session.get(
                url,
                params={"document": cpf_limpo},
                headers=self.headers,
                auth=self.auth,
                timeout=(3, 10),
            )

            if response.status_code == 404:
                logger.warning("Cupom não encontrado no ConectaHub para o documento %s", cpf_limpo)
                return None

            response.raise_for_status()
            data = response.json()

            logger.info("Resposta do ConectaHub para CPF %s: %s", cpf_limpo, data)
            return self._extrair_dados(data)

        except requests.RequestException as err:
            logger.error("Erro ao buscar cupom no ConectaHub após tentativas (%s): %s", url, err)
            return None

    def _extrair_dados(self, data):
        if not data:
            return None

        if isinstance(data, list):
            return data[0] if len(data) > 0 else None

        if isinstance(data, dict):
            conteudo = (
                data.get("dados")
                or data.get("data")
                or data.get("cupons")
                or data.get("resultado")
            )
            if conteudo is not None:
                return self._extrair_dados(conteudo)
            if len(data) > 0:
                return data

        return None

    def obter_proximo_id_transacao(self) -> int | None:
        url = f"{self.base_url}/transacao/proximo-id"

        try:
            response = self.session.get(
                url, headers=self.headers, auth=self.auth, timeout=(3, 10)
            )
            response.raise_for_status()
            dados = response.json()

            if isinstance(dados, dict):
                return dados.get("id_transacao")
            return dados

        except requests.RequestException as err:
            logger.error("Erro ao obter próximo ID de transação (%s): %s", url, err)
            return None

    def atualizar_cupom_utilizado(self, redeem_coupon_id: str, user_id: str):
        url = f"{self.base_url}/cupons/utilizar"
        payload = {"redeem_coupon_id": redeem_coupon_id, "user_id": user_id}

        try:
            response = self.session.post(
                url, json=payload, headers=self.headers, auth=self.auth, timeout=(3, 10)
            )
            response.raise_for_status()
            return response.json()

        except requests.RequestException as err:
            logger.error("Erro ao atualizar cupom como utilizado (%s): %s", url, err)
            return None