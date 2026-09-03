import os

import requests


class AutenticacaoRepository:

    def __init__(self, base_url: str | None = None):
        self.base_url = (
            base_url
            or os.getenv(
                "CONECTAHUB_URL",
                "https://conectahub-internal.sacavalcante.com.br/api/v1/liberacao-estacionamento"
            ).rstrip("/")
        )
        self.headers = {"Content-Type": "application/json"}

    def buscar_usuario(self, usuario: str):
        url = f"{self.base_url}/busca-usuario"

        response = requests.post(
            url, params={"usuario": usuario}, headers=self.headers, timeout=10
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()