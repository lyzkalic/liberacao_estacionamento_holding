import logging
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from backend.dependencies import exigir_admin
from models.schema import AuditoriaFiltroRequest
from services.auditoria_service import AuditoriaService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Auditoria"])
templates = Jinja2Templates(directory="frontend/pages")
service = AuditoriaService()


@router.get("/auditoria", response_class=HTMLResponse)
async def tela_auditoria(
    request: Request,
    usuario_logado: Annotated[dict, Depends(exigir_admin)],
):
    try:
        return templates.TemplateResponse(
            request=request,
            name="auditoria.html",
            context={
                "usuario": usuario_logado,
                "perfil": usuario_logado.get("perfil"),
            },
        )
    except Exception:
        logger.exception("Erro ao renderizar a tela de auditoria")
        raise


@router.post("/auditoria/pesquisar")
async def pesquisar_auditoria(
    filtros: AuditoriaFiltroRequest,
    usuario_logado: Annotated[dict, Depends(exigir_admin)],
):
    registros = service.listar_historico(
        cpf=filtros.cpf,
        usuario=filtros.usuario,
        status=filtros.status,
        data_inicial=filtros.data_inicial,
        data_final=filtros.data_final,
    )

    return {"sucesso": True, "dados": registros}


@router.get("/auditoria/exportar")
async def exportar_auditoria(
    usuario_logado: Annotated[dict, Depends(exigir_admin)],
    cpf: str | None = None,
    usuario: str | None = None,
    status: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
):
    try:
        buffer = service.exportar_historico(
            cpf=cpf,
            usuario=usuario,
            status=status,
            data_inicial=data_inicial,
            data_final=data_final,
        )

        data_formatada = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")
        nome_arquivo = f"auditoria_estacionamento_{data_formatada}.xlsx"

        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'},
        )

    except Exception:
        logger.exception("Erro ao exportar a auditoria para Excel")
        raise