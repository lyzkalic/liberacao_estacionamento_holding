import os
<<<<<<< HEAD

=======
>>>>>>> eda019813909102135d79eece075129c34643f43
import requests


class AutenticacaoRepository:

<<<<<<< HEAD
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
=======
  def __init__(self, base_url: str = None):
    self.base_url = (
        base_url
        or os.getenv(
            "CONECTA_HUB_URL",
            "https://conectahub.sacavalcante.com.br/api/v1",
        ).rstrip("/")
    )

  def buscar_usuario(self, usuario: str) -> dict:
    """GET: Busca informações do usuário pelo username na nova API."""
    url = f"{self.base_url}/liberação-de-estacionamento/usuarios"

    try:
      response = requests.get(url, params={"usuario": usuario}, timeout=10)

      if response.status_code == 200:
        # Retorna o dicionário com os dados do usuário (id, perfil, ativo, etc.)
        return response.json()

      return None

    except requests.exceptions.RequestException:
      return None
>>>>>>> eda019813909102135d79eece075129c34643f43
