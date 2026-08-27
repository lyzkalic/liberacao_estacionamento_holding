import os
import requests


class AuditoriaRepository:

  def __init__(self, base_url: str = None, token: str = None):
    # Configura a URL da API (pode vir de variável de ambiente)
    self.base_url = (
        base_url
        or os.getenv("CONECTA_HUB_URL", "https://conectahub.sacavalcante.com.br/api/v1/liberação-de-estacionamento").rstrip("/")
    )
    self.headers = {"Content-Type": "application/json"}
    if token:
      self.headers["Authorization"] = f"Bearer {token}"

  def registrar(
      self,
      usuario_id,
      tipo_acao,
      cpf_cliente,
      numero_ticket,
      id_transacao,
      cupom_id,
      resultado,
      mensagem,
      id_garagem=None,
  ):
    url = f"{self.base_url}/historico-liberacao" # Definir endpoint no conectahub

    # Converte os dados que iriam no INSERT em um dicionário (JSON Body)
    payload = {
        "usuario_id": usuario_id,
        "tipo_acao": tipo_acao,
        "cpf_cliente": cpf_cliente,
        "numero_ticket": numero_ticket,
        "id_transacao": id_transacao,
        "cupom_id": cupom_id,
        "resultado": resultado,
        "mensagem": mensagem,
        "id_garagem": id_garagem,
    }

    response = requests.post(
        url, json=payload, headers=self.headers, timeout=10
    )
    response.raise_for_status()

    return response.json()

  def listar_historico(
      self,
      cpf=None,
      usuario=None,
      status=None,
      data_inicial=None,
      data_final=None,
  ):
    url = f"{self.base_url}/historico-liberacao"

    # Monta os Query Parameters para a consulta GET (substitui a cláusula WHERE)
    params = {}
    if cpf:
      params["cpf"] = cpf
    if usuario:
      params["usuario"] = usuario
    if status:
      params["status"] = status
    if data_inicial:
      params["data_inicial"] = str(data_inicial)
    if data_final:
      params["data_final"] = str(data_final)

    response = requests.get(
        url, params=params, headers=self.headers, timeout=10
    )
    response.raise_for_status()

    # O retornos .json() já entrega uma lista de dicionários igual ao RealDictCursor
    return response.json()

  def exportar_historico(
      self,
      cpf=None,
      usuario=None,
      status=None,
      data_inicial=None,
      data_final=None,
  ):
    return self.listar_historico(
        cpf=cpf,
        usuario=usuario,
        status=status,
        data_inicial=data_inicial,
        data_final=data_final,
    )