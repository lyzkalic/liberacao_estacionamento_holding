import os
import requests


class CupomRepository:

    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = (
            base_url
            or os.getenv(
                "CONECTA_HUB_URL",
                "https://conectahub-internal.sacavalcante.com.br/api/v1/liberacao-estacionamento",
            ).rstrip("/")
        )
        self.headers = {"Content-Type": "application/json"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def buscar_cupom(self, cpf: str):
        url = f"{self.base_url}/cupons/buscar"
        response = requests.get(
            url, params={"cpf": cpf}, headers=self.headers, timeout=10
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()

    def obter_proximo_id_transacao() -> int:
        url = f"{self.base_url}/transacao/proximo-id"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json().get("id_transacao")

    def atualizar_cupom_utilizado(self, redeem_coupon_id: int, user_id: int):
        url = f"{self.base_url}/cupons/utilizar"
        payload = {"redeem_coupon_id": redeem_coupon_id, "user_id": user_id}
        response = requests.post(
            url, json=payload, headers=self.headers, timeout=10
        )
        response.raise_for_status()
        return response.json()