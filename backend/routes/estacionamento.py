import logging
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.dependencies import exigir_login
from models.schema import BuscarCpfRequest, LiberarTicketRequest
from services.cupom_service import CupomService

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="frontend/pages")
service = CupomService()


@router.get("/", response_class=HTMLResponse)
async def tela_buscar_cpf(request: Request, usuario=Depends(exigir_login)):
    erro = request.session.pop("erro_acesso", None)

    return templates.TemplateResponse(
        request=request,
        name="buscar_cpf.html",
        context={"perfil": usuario["perfil"], "erro": erro}
    )


@router.get("/liberar", response_class=HTMLResponse)
async def tela_liberar(request: Request, usuario=Depends(exigir_login)):
    return templates.TemplateResponse(
        request=request,
        name="liberar_ticket.html"
    )


@router.post("/buscar-cupom")
async def buscar_cupom(request: BuscarCpfRequest, usuario=Depends(exigir_login)):
    try:
        resultado = service.buscar_cupom(usuario_id=usuario["usuario_id"], cpf=request.cpf)

        if resultado:
            return {
                "sucesso": True,
                "dados": resultado
            }

        return {
            "sucesso": False,
            "mensagem": "Nenhum cupom encontrado."
        }

    except Exception:
        logger.exception("Erro ao buscar cupom para o CPF %s", request.cpf)
        raise


@router.post("/liberar-ticket")
async def liberar_ticket(request: LiberarTicketRequest, usuario=Depends(exigir_login)):
    try:
        resultado = service.liberar_ticket(
            usuario_id=usuario["usuario_id"],
            cpf=request.cpf,
            numero_ticket=request.numero_ticket
        )
        return resultado

    except Exception:
        logger.exception("Erro ao liberar o ticket %s para o CPF %s", request.numero_ticket, request.cpf)
        raise