"""Cliente da API ConectaHub para as rotas de liberação de estacionamento."""

import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()

_BASE_URL = os.getenv(
    "CONECTAHUB_BASE_URL", "https://conectahub-internal.sacavalcante.com.br"
)
_USER = os.getenv("CONECTAHUB_USER", "psqladmin")
_PASSWORD = os.getenv("CONECTAHUB_PASSWORD", "")

_log = logging.getLogger("conectahub")


class ConectaHubClient:
    """Cliente para os endpoints `liberacao-estacionamento` da API ConectaHub."""

    def __init__(
        self,
        base_url: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ):
        self._base_url = (base_url or _BASE_URL).rstrip("/")
        self._auth = (user or _USER, password if password is not None else _PASSWORD)
        self._session = requests.Session()

    def _request(self, method: str, rota: str, **kwargs) -> dict:
        url = f"{self._base_url}/api/v1/liberacao-estacionamento/{rota}"
        try:
            resp = self._session.request(
                method, url, auth=self._auth, timeout=30, **kwargs
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            _log.error("Falha na chamada %s %s | erro=%s", method, url, exc, exc_info=True)
            raise

    def buscar_cupom(self, document: str, coupon_id: str | None = None) -> dict:
        params = {"document": document}
        if coupon_id is not None:
            params["coupon_id"] = coupon_id
        return self._request("GET", "buscar-cupom", params=params)

    def buscar_usuario(self, usuario: str) -> dict:
        return self._request("GET", "busca-usuario", params={"usuario": usuario})

    def marcar_cupom_usado(self, payload: dict) -> dict:
        return self._request("PATCH", "marca-cupomusado", json=payload)

    def obter_proximo_id_transacao(self) -> dict:
        return self._request("GET", "obter-proximo-id-transacao")