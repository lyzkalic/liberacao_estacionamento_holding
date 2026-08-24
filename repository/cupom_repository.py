import requests

class CupomRepository:

    def __init__(self):
        self.base_url = (
            "https://conectahub-internal.sacavalcante.com.br"
            "/api/v1/liberação-de-estacionamento"
        )

    def buscar_cupom(self, document):
        """
        GET
        Busca um cupom de isenção de estacionamento
        pelo documento do cliente.
        """

        url = f"{self.base_url}/buscar-cupom"

        response = requests.get(
            url,
            params={
                "document": document
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def atualizar_cupom_utilizado(
        self,
        redeem_coupon_id,
        user_id
    ):
        """
        PATCH
        Marca o cupom como utilizado.
        """

        url = f"{self.base_url}/marca-cupomusado"

        payload = {
            "redeem_coupon_id": redeem_coupon_id,
            "user_id": user_id
        }

        response = requests.patch(
            url,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def obter_proximo_id_transacao(self):
        """
        GET
        Obtém o próximo ID de transação.
        """

        url = f"{self.base_url}/obter-próximo-id-transação"

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()
