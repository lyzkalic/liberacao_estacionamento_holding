import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from repository.auditoria_repository import AuditoriaRepository
from models.schema import LoginRequest
from services.autenticacao_service import AutenticacaoService

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="frontend/pages")
service = AutenticacaoService()


# Tela de login
@router.get("/login", response_class=HTMLResponse)
async def tela_login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


# Login
@router.post("/login")
async def login(request: Request, dados: LoginRequest):

    try:

        resultado = service.autenticar(dados.usuario, dados.senha)

        if not resultado["sucesso"]:

            return {
                "sucesso": False,
                "mensagem": resultado["mensagem"]
            }

        request.session["usuario_id"] = resultado["usuario_id"]
        request.session["usuario"] = resultado["usuario"]
        request.session["perfil"] = resultado["perfil"]

        AuditoriaRepository().registrar(
         usuario_id=resultado["usuario_id"],
         tipo_acao="LOGIN",
         cpf_cliente="-",
         numero_ticket="-",
         id_transacao=None,
         cupom_id=None,
         resultado="SUCESSO",
         mensagem=f'Login realizado pelo usuário {resultado["usuario"]}',
         id_garagem=None
        )

        return {
            "sucesso": True,
            "mensagem": "Login realizado com sucesso."
        }

    except Exception:

        logger.exception("Erro ao autenticar o usuário %s", dados.usuario)
        raise


# Logout
@router.get("/logout")
async def logout(request: Request):

    logger.info("Logout: usuário %s", request.session.get("usuario"))

    request.session.clear()

    return RedirectResponse("/login")
