import os
import requests


class AutenticacaoService:

  def __init__(self, base_url: str = None):
    self.base_url = (
        base_url
        or os.getenv(
            "CONECTA_HUB_URL",
            "https://conectahub-internal.sacavalcante.com.br/api/v1",
        ).rstrip("/")
    )

  def autenticar(self, usuario: str, senha: str) -> dict:
    url = f"{self.base_url}/auth/login"

    # Envia o usuário e senha no corpo da requisição POST
    payload = {"usuario": usuario, "senha": senha}

    try:
      response = requests.post(
          url, json=payload, headers={"Content-Type": "application/json"}, timeout=10
      )

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
        erro = response.json()
        return {
            "sucesso": False,
            "mensagem": erro.get("mensagem", "Usuário ou senha inválidos."),
        }

      return {
          "sucesso": False,
          "mensagem": f"Erro na API de autenticação ({response.status_code}).",
      }

    except requests.exceptions.RequestException as e:
      return {
          "sucesso": False,
          "mensagem": "Falha de conexão com o servidor de autenticação.",
      }
