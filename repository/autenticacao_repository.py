import requests

class AutenticacaoRepository:

    def buscar_usuario(self, usuario):

        response = requests.get(
            "https://conectahub-internal.sacavalcante.com.br/api/v1/liberação-de-estacionamento/busca-usuário",
            params={"usuario":usuario},
            timeout=10
        )

        if resoponse.status_code == 404:
            return None

            response.raise_for_status()

            return response.json()