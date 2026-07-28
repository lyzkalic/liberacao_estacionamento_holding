import logging

import bcrypt

from repository.autenticacao_repository import AutenticacaoRepository

logger = logging.getLogger(__name__)


class AutenticacaoService:

    def __init__(self):

        self.repository = AutenticacaoRepository()

    def autenticar(self, usuario, senha):

        login = usuario.split("@")[0].strip().lower() if "@" in usuario else usuario.strip().lower()

        usuario_encontrado = self.repository.buscar_usuario(login)

        if not usuario_encontrado:

            logger.warning("Tentativa de login com usuário inexistente: %s", usuario)

            return {
                "sucesso": False,
                "mensagem": "Usuário ou senha inválidos"
            }

        if not usuario_encontrado["ativo"]:

            logger.warning("Tentativa de login em usuário inativo: %s", usuario)

            return {
                "sucesso": False,
                "mensagem": "Usuário inativo."
            }

        senha_valida = bcrypt.checkpw(
            senha.encode("utf-8"),
            usuario_encontrado["senha_hash"].encode("utf-8")
        )

        if not senha_valida:

            logger.warning("Senha inválida para o usuário %s", usuario)

            return {
                "sucesso": False,
                "mensagem": "Usuário ou senha inválidos"
            }

        logger.info(
            "Login realizado: usuário %s (perfil %s)",
            usuario_encontrado["usuario"],
            usuario_encontrado["perfil"]
        )

        return {
            "sucesso": True,
            "usuario_id": usuario_encontrado["id"],
            "usuario": usuario_encontrado["usuario"],
            "perfil": usuario_encontrado["perfil"]
        }
