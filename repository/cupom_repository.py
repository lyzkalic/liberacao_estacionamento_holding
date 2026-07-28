import psycopg2.extras

from backend.database import conectar


class CupomRepository:

    CUPOM_ID = "150e6802-54e3-49a5-b2eb-a1357327e10c"

    def buscar_cupom(self, cpf):

        conexao = conectar()

        try:

            cursor = conexao.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )

            sql = """
                SELECT
                    c.name AS cliente_nome,
                    u.id AS user_id,
                    rc.id AS redeem_coupon_id,
                    rc.code,
                    rc.coupon_id,
                    rc.has_used,
                    cp.title AS beneficio,
                    cp.description AS descricao_beneficio
                FROM customer c
                INNER JOIN users u
                    ON u.customer_id = c.id
                INNER JOIN redeem_coupons rc
                    ON rc.user_id = u.id
                INNER JOIN coupon cp
                    ON cp.id = rc.coupon_id
                WHERE c.document = %s
                  AND rc.coupon_id = %s
                  AND rc.has_used = false;
            """

            cursor.execute(
                sql,
                (
                    cpf,
                    self.CUPOM_ID
                )
            )

            resultado = cursor.fetchone()

            return resultado

        finally:

            cursor.close()
            conexao.close()

    def obter_proximo_id_transacao(self):

        conexao = conectar()

        try:

            cursor = conexao.cursor()

            cursor.execute(
                "SELECT nextval('wps_id_transacao_seq');"
            )

            resultado = cursor.fetchone()

            return resultado[0]

        finally:

            cursor.close()
            conexao.close()

    def atualizar_cupom_utilizado(self, redeem_coupon_id, user_id):

        conexao = conectar()

        try:

            cursor = conexao.cursor()

            sql = """
                UPDATE redeem_coupons
                SET has_used = true
                WHERE id = %s
                  AND user_id = %s;
            """

            cursor.execute(sql, (redeem_coupon_id, user_id))

            conexao.commit()

        finally:

            cursor.close()
            conexao.close()