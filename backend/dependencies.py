from fastapi import Depends, Request


class NaoAutenticadoException(Exception):
    pass


class AcessoNegadoException(Exception):
    pass


def exigir_login(request: Request) -> dict:
    # Obtém o dicionário salvo na chave 'usuario'
    usuario = request.session.get("usuario")

    # Se a sessão não existir ou não tiver usuario_id, lança exceção
    if not usuario or not usuario.get("usuario_id"):
        raise NaoAutenticadoException()

    return usuario


def exigir_admin(usuario: dict = Depends(exigir_login)) -> dict:
    if usuario.get("perfil") != "ADMIN":
        raise AcessoNegadoException()

    return usuario