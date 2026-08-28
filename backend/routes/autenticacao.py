import os
import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.autenticacao_service import AutenticacaoService

logger = logging.getLogger(__name__)

# Certifique-se de NÃO passar prefix="/login" aqui
router = APIRouter(tags=["Autenticação"])
auth_service = AutenticacaoService()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGIN_HTML_PATH = os.path.join(BASE_DIR, "frontend", "pages", "login.html")


class LoginSchema(BaseModel):
    usuario: str
    senha: str


@router.get("/login")
async def exibir_login():
    if not os.path.exists(LOGIN_HTML_PATH):
        raise HTTPException(status_code=404, detail="Arquivo frontend/login.html não encontrado.")
    return FileResponse(LOGIN_HTML_PATH)


@router.post("/login")
def login(dados: LoginSchema):
    resultado = auth_service.autenticar(dados.usuario, dados.senha)

    if not resultado.get("sucesso"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=resultado.get("mensagem", "Usuário ou senha inválidos."),
        )

        request.session["usuario"] = {
        "id": resultado.get("usuario_id"),
        "usuario": resultado.get("usuario"),
        "perfil": resultado.get("perfil"),
    }

    return {"sucesso": True, "redirect_url": "/buscar"}