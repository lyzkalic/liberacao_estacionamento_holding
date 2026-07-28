from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class WpsResponse:
    sucesso: bool
    status_http: Optional[int]
    mensagem: str
    resposta: Any
