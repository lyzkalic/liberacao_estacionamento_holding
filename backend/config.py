import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ConectaHub API
    CONECTAHUB_API_URL = os.getenv("CONECTA_HUB_URL")

    # Integracao WPS
    WPS_URL = os.getenv("WPS_URL")
    WPS_SECRET_KEY = os.getenv("WPS_SECRET_KEY")
    WPS_API_KEY_ID = os.getenv("WPS_API_KEY_ID")
    WPS_TIMEOUT = int(os.getenv("WPS_TIMEOUT", 10))
    WPS_UDID = os.getenv("WPS_UDID")
    WPS_IP = os.getenv("WPS_IP")
    WPS_BANDEIRA = os.getenv("WPS_BANDEIRA")
    WPS_PORTADOR = os.getenv("WPS_PORTADOR")
    WPS_CARTAO = os.getenv("WPS_CARTAO")
    WPS_VALIDADE = os.getenv("WPS_VALIDADE")
    WPS_ID_PROMOCAO = int(os.getenv("WPS_ID_PROMOCAO", 0))
    WPS_ID_GARAGEM = int(os.getenv("WPS_ID_GARAGEM", 0))

    # Sessao
    SESSION_SECRET = os.getenv("SESSION_SECRET")

    # Ambiente / Log
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"