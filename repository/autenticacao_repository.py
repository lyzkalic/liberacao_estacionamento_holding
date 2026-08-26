import os
import requests


class AutenticacaoRepository:

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
