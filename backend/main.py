import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from backend.config import Config
from backend.dependencies import AcessoNegadoException, NaoAutenticadoException
from backend.logging_config import configurar_logging
from backend.routes.estacionamento import router
from backend.routes.autenticacao import router as auth_router
from backend.routes.auditoria import router as auditoria_router

configurar_logging()

logger = logging.getLogger(__name__)


app = FastAPI(

    title="Liberação de Estacionamento",

    version="1.0.0"

)


app.add_middleware(SessionMiddleware, secret_key=Config.SESSION_SECRET)


@app.exception_handler(NaoAutenticadoException)
async def nao_autenticado_handler(request: Request, exc: NaoAutenticadoException):

    return RedirectResponse("/login", status_code=303)


@app.exception_handler(AcessoNegadoException)
async def acesso_negado_handler(request: Request, exc: AcessoNegadoException):

    request.session["erro_acesso"] = "Acesso restrito a administradores."

    return RedirectResponse("/", status_code=303)


# Qualquer exceção não tratada nas rotas cai aqui: loga o traceback completo
# (terminal + arquivo de log) e responde com JSON, nunca texto puro.
@app.exception_handler(Exception)
async def erro_interno_handler(request: Request, exc: Exception):

    logger.exception("Erro não tratado em %s %s", request.method, request.url.path)

    conteudo = {
        "sucesso": False,
        "mensagem": "Erro interno ao processar a solicitação."
    }

    if Config.DEBUG:
        conteudo["erro"] = str(exc)

    return JSONResponse(status_code=500, content=conteudo)


app.mount(

    "/css",

    StaticFiles(directory="frontend/css"),

    name="css"

)

app.mount(

    "/js",

    StaticFiles(directory="frontend/js"),

    name="js"

)

app.mount(

    "/assets",

    StaticFiles(directory="frontend/assets"),

    name="assets"

)


app.include_router(router)
app.include_router(auth_router)
app.include_router(auditoria_router)


@app.get("/")

async def home():

    return RedirectResponse("/buscar")
