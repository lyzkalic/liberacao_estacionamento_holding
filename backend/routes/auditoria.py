import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from backend.dependencies import exigir_admin
from models.schema import AuditoriaFiltroRequest
from services.auditoria_service import AuditoriaService

logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="frontend/pages")

service = AuditoriaService()


# Tela de auditoria
@router.get("/auditoria", response_class=HTMLResponse)
async def tela_auditoria(request: Request, usuario_logado=Depends(exigir_admin)):

    try:

        return templates.TemplateResponse(
            request=request,
            name="auditoria.html"
        )

    except Exception:

        logger.exception("Erro ao renderizar a tela de auditoria")
        raise


# Pesquisar histórico
@router.post("/auditoria/pesquisar")
async def pesquisar_auditoria(filtros: AuditoriaFiltroRequest, usuario_logado=Depends(exigir_admin)):

    registros = service.listar_historico(
        cpf=filtros.cpf,
        usuario=filtros.usuario,
        status=filtros.status,
        data_inicial=filtros.data_inicial,
        data_final=filtros.data_final
    )

    return {
        "sucesso": True,
        "dados": registros
    }


# Exportar Excel
@router.get("/auditoria/exportar")
async def exportar_auditoria(
    usuario_logado=Depends(exigir_admin),
    cpf: str = None,
    usuario: str = None,
    status: str = None,
    data_inicial: str = None,
    data_final: str = None
):

    try:

        buffer = service.exportar_historico(
            cpf=cpf,
            usuario=usuario,
            status=status,
            data_inicial=data_inicial,
            data_final=data_final
        )

        nome_arquivo = f"auditoria_estacionamento_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"

        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'}
        )

    except Exception:

        logger.exception("Erro ao exportar a auditoria para Excel")
        raise
