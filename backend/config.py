import psycopg2
from backend.config import Config

def conectar():
    print("HOST:", Config.DB_HOST)
    print("PORT:", Config.DB_PORT)
    print("DATABASE:", Config.DB_NAME)
    print("USER:", Config.DB_USER)

    return psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        sslmode="require",
        connect_timeout=5
    )
