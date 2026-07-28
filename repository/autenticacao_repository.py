import psycopg2.extras

from backend.database import conectar


class AutenticacaoRepository:

    def buscar_usuario(self, usuario):

        conexao = conectar()

        try:

            cursor = conexao.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )

            sql = """
                SELECT
                    id,
                    usuario,
                    senha_hash,
                    perfil,
                    ativo
                FROM autenticacao_estacionamento
                WHERE usuario = %s;
            """

            cursor.execute(sql, (usuario,))

            return cursor.fetchone()

        finally:

            cursor.close()
            conexao.close()
