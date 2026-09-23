import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # ConectaHub API
    CONECTAHUB_API_URL = os.getenv("CONECTAHUB_URL", "https://conectahub-internal.sacavalcante.com.br")
    CONECTAHUB_USER = os.getenv("CONECTAHUB_USER", "psqladmin")
    CONECTAHUB_PASSWORD = os.getenv("CONECTAHUB_PASSWORD", "")

    # Integração WPS
    WPS_URL = os.getenv("WPS_URL")
    WPS_SECRET_KEY = os.getenv("WPS_SECRET_KEY")
    WPS_API_KEY_ID = os.getenv("WPS_API_KEY_ID")
    WPS_TIMEOUT = int(os.getenv("WPS_TIMEOUT", "10"))

    # Sessão
    SESSION_SECRET = os.getenv("SESSION_SECRET")

    # Ambiente / Log
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"