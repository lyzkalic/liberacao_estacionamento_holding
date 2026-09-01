import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from backend.config import Config
from backend.dependencies import AcessoNegadoException, NaoAutenticadoException
from backend.logging_config import configurar_logging
from backend.routes.auditoria import router as auditoria_router
from backend.routes.autenticacao import router as auth_router
from backend.routes.estacionamento import router as estacionamento_router

# Inicializa as configurações de log
configurar_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Liberação de Estacionamento",
    version="1.0.0"
)

# Middleware de Sessão (com suporte a ambiente local HTTP)
secret_key = getattr(Config, "SESSION_SECRET", None) or "chave-secreta-temporaria-dev"
app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key,
    same_site="lax",
    https_only=False  # Permite que o cookie de sessão seja salvo sem HTTPS durante o desenvolvimento
)

# --- TRATAMENTO DE EXCEÇÕES ---

@app.exception_handler(NaoAutenticadoException)
async def nao_autenticado_handler(request: Request, exc: NaoAutenticadoException):
    return RedirectResponse("/login", status_code=303)


@app.exception_handler(AcessoNegadoException)
async def acesso_negado_handler(request: Request, exc: AcessoNegadoException):
    request.session["erro_acesso"] = "Acesso restrito a administradores."
    return RedirectResponse("/", status_code=303)


@app.exception_handler(Exception)
async def erro_interno_handler(request: Request, exc: Exception):
    logger.exception("Erro não tratado em %s %s", request.method, request.url.path)

    conteudo = {
        "sucesso": False,
        "mensagem": "Erro interno ao processar a solicitação."
    }

    if getattr(Config, "DEBUG", False):
        conteudo["erro"] = str(exc)

    return JSONResponse(status_code=500, content=conteudo)


# --- ARQUIVOS ESTÁTICOS ---
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")


# --- REGISTRO DAS ROTAS ---

app.include_router(auth_router)
app.include_router(estacionamento_router)
app.include_router(auditoria_router)


# --- ROTA RAIZ ---

@app.get("/")
async def home(request: Request):
    if not request.session.get("usuario"):
        return RedirectResponse("/login", status_code=303)

    return RedirectResponse("/buscar", status_code=303)