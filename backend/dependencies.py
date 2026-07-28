from fastapi import Depends, Request

from backend.database import conectar


def get_db():

    conexao = conectar()

    try:

        yield conexao

    finally:

        conexao.close()


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
        "perfil": request.session.get("perfil")
    }


def exigir_admin(usuario=Depends(exigir_login)):

    if usuario["perfil"] != "ADMIN":

        raise AcessoNegadoException()

    return usuario
