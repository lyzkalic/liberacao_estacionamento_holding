import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class AuditoriaRepository:

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

        user = usuario or os.getenv("CONECTAHUB_USER", "psqladmin")
        password = senha or os.getenv("CONECTAHUB_PASSWORD", "")

        self.auth = (user, password)
        self.headers = {"Content-Type": "application/json"}

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
        url = f"{self.base_url}/historico-liberacao"

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

        try:
            response = requests.post(
                url, json=payload, headers=self.headers, auth=self.auth, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as err:
            logger.error("Falha ao registrar auditoria no ConectaHub (%s): %s", url, err)
            return None

    def listar_historico(
        self,
        cpf: str | None = None,
        usuario: str | None = None,
        status: str | None = None,
        data_inicial: str | None = None,
        data_final: str | None = None,
    ):
        url = f"{self.base_url}/historico-liberacao"

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

        try:
            response = requests.get(
                url, params=params, headers=self.headers, auth=self.auth, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as err:
            logger.error("Falha ao listar histórico de auditoria: %s", err)
            return []

    def exportar_historico(
        self,
        cpf: str | None = None,
        usuario: str | None = None,
        status: str | None = None,
        data_inicial: str | None = None,
        data_final: str | None = None,
    ):
        return self.listar_historico(
            cpf=cpf,
            usuario=usuario,
            status=status,
            data_inicial=data_inicial,
            data_final=data_final,
        )