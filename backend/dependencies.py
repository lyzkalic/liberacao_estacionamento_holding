from typing import Annotated

from fastapi import Depends, Request


class NaoAutenticadoException(Exception):
    pass


class AcessoNegadoException(Exception):
    pass


def exigir_login(request: Request) -> dict:
    usuario = request.session.get("usuario")

    if not usuario or not usuario.get("usuario_id"):
        raise NaoAutenticadoException()

    return usuario


# Uso do Annotated para resolver o Ruff(B008)
def exigir_admin(usuario: Annotated[dict, Depends(exigir_login)]) -> dict:
    if usuario.get("perfil") != "ADMIN":
        raise AcessoNegadoException()

    return usuario