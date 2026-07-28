import psycopg2.extras

from backend.database import conectar


class AuditoriaRepository:

    def registrar(self, usuario_id, tipo_acao, cpf_cliente, numero_ticket, id_transacao, cupom_id, resultado, mensagem, id_garagem=None):

        conexao = conectar()

        try:

            cursor = conexao.cursor()

            sql = """
                INSERT INTO historico_liberacao_estacionamento
                    (usuario_id, tipo_acao, cpf_cliente, numero_ticket, id_transacao, cupom_id, resultado, mensagem, id_garagem)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            cursor.execute(
                sql,
                (
                    usuario_id,
                    tipo_acao,
                    cpf_cliente,
                    numero_ticket,
                    id_transacao,
                    cupom_id,
                    resultado,
                    mensagem,
                    id_garagem
                )
            )

            conexao.commit()

        finally:

            cursor.close()
            conexao.close()

    def listar_historico(self, cpf=None, usuario=None, status=None, data_inicial=None, data_final=None):

        conexao = conectar()

        try:

            cursor = conexao.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )

            sql = """
                SELECT
                    h.data_liberacao,
                    au.usuario,
                    au.perfil,
                    h.tipo_acao,
                    h.cpf_cliente,
                    h.numero_ticket,
                    h.id_transacao,
                    h.id_garagem,
                    h.resultado,
                    h.mensagem
                FROM historico_liberacao_estacionamento h
                LEFT JOIN autenticacao_estacionamento au
                    ON au.id = h.usuario_id
                WHERE 1=1
            """

            parametros = []

            if cpf:
                sql += " AND h.cpf_cliente = %s"
                parametros.append(cpf)

            if usuario:
                sql += " AND au.usuario ILIKE %s"
                parametros.append(f"%{usuario}%")

            if status:
                sql += " AND h.resultado ILIKE %s"
                parametros.append(f"%{status}%")

            if data_inicial:
                sql += " AND h.data_liberacao::date >= %s"
                parametros.append(data_inicial)

            if data_final:
                sql += " AND h.data_liberacao::date <= %s"
                parametros.append(data_final)

            sql += " ORDER BY h.data_liberacao DESC;"

            cursor.execute(sql, tuple(parametros))

            return cursor.fetchall()

        finally:

            cursor.close()
            conexao.close()

    def exportar_historico(self, cpf=None, usuario=None, status=None, data_inicial=None, data_final=None):

        return self.listar_historico(
            cpf=cpf,
            usuario=usuario,
            status=status,
            data_inicial=data_inicial,
            data_final=data_final
        )
