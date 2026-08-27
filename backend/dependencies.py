from fastapi import Depends, Request


class NaoAutenticadoException(Exception):
    pass


class AcessoNegadoException(Exception):
    pass


def exigir_login(request: Request):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        raise NaoAutenticadoException()

    return {
        "usuario_id": usuario_id,
        "usuario": request.session.get("usuario"),
        "perfil": request.session.get("perfil"),
    }


def exigir_admin(usuario=Depends(exigir_login)):
    if usuario.get("perfil") != "ADMIN":
        raise AcessoNegadoException()

    return usuario