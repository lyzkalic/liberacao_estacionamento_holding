import logging
import requests
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.schema import LoginRequest
from repository.auditoria_repository import AuditoriaRepository
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
        # O service.autenticar fará uma chamada HTTP POST para a nova API de autenticação
        resultado = service.autenticar(dados.usuario, dados.senha)

        if not resultado.get("sucesso"):
            return {
                "sucesso": False,
                "mensagem": resultado.get("mensagem", "Credenciais inválidas.")
            }

        # Armazena os dados do usuário na sessão
        request.session["usuario_id"] = resultado["usuario_id"]
        request.session["usuario"] = resultado["usuario"]
        request.session["perfil"] = resultado["perfil"]

        # Armazena o token retornado pela nova API para usar nas chamadas das páginas protegidas
        if "token" in resultado:
            request.session["token"] = resultado["token"]

        # Registra auditoria enviando POST para a nova API via AuditoriaRepository
        try:
            token = request.session.get("token")
            AuditoriaRepository(token=token).registrar(
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
        except Exception as audit_err:
            # Evita que uma falha ao gravar a auditoria na API externa interrompa a sessão de login
            logger.error("Erro ao registrar auditoria via HTTP: %s", audit_err)

        return {
            "sucesso": True,
            "mensagem": "Login realizado com sucesso."
        }

    except requests.exceptions.RequestException as http_err:
        logger.error("Erro de comunicação HTTP com a API durante o login: %s", http_err)
        return {
            "sucesso": False,
            "mensagem": "Serviço de autenticação temporariamente indisponível."
        }
    except Exception:
        logger.exception("Erro ao autenticar o usuário %s", dados.usuario)
        raise


# Logout
@router.get("/logout")
async def logout(request: Request):
    logger.info("Logout: usuário %s", request.session.get("usuario"))

    request.session.clear()

    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)