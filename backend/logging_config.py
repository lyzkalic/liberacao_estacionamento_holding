import logging
import os

from backend.config import Config


def configurar_logging():

    os.makedirs("logs", exist_ok=True)

    nivel = logging.DEBUG if Config.DEBUG else logging.INFO

    logging.basicConfig(
        level=nivel,
        format="%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/app.log", encoding="utf-8")
        ],
        force=True
    )
