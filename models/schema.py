from typing import Optional

from pydantic import BaseModel

class BuscarCpfRequest(BaseModel):
    cpf: str

class LiberarTicketRequest(BaseModel):
    cpf: str
    numero_ticket: str

class LoginRequest(BaseModel):
    usuario: str
    senha: str

class AuditoriaFiltroRequest(BaseModel):
    cpf: Optional[str] = None
    usuario: Optional[str] = None
    status: Optional[str] = None
    data_inicial: Optional[str] = None
    data_final: Optional[str] = None