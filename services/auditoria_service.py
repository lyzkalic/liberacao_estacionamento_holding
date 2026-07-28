import io
import logging

import openpyxl

from repository.auditoria_repository import AuditoriaRepository

logger = logging.getLogger(__name__)


class AuditoriaService:

    COLUNAS = ["Data/Hora", "Usuário", "Perfil", "CPF Cliente", "Número Ticket", "ID Transação", "ID Garagem", "Resultado", "Mensagem"]

    def __init__(self):

        self.repository = AuditoriaRepository()

    def listar_historico(self, cpf=None, usuario=None, status=None, data_inicial=None, data_final=None):

        logger.info(
            "Listando histórico de auditoria (filtros: cpf=%s, usuario=%s, status=%s, data_inicial=%s, data_final=%s)",
            cpf, usuario, status, data_inicial, data_final
        )

        return self.repository.listar_historico(
            cpf=cpf,
            usuario=usuario,
            status=status,
            data_inicial=data_inicial,
            data_final=data_final
        )

    def exportar_historico(self, cpf=None, usuario=None, status=None, data_inicial=None, data_final=None):

        logger.info("Exportação do Excel iniciada")

        registros = self.repository.exportar_historico(
            cpf=cpf,
            usuario=usuario,
            status=status,
            data_inicial=data_inicial,
            data_final=data_final
        )

        buffer = self.gerar_excel(registros)

        logger.info("Exportação do Excel concluída (%s registros)", len(registros))

        return buffer

    def gerar_excel(self, registros):

        planilha = openpyxl.Workbook()

        aba = planilha.active
        aba.title = "Auditoria"

        aba.append(self.COLUNAS)

        for registro in registros:

            data_liberacao = registro["data_liberacao"]

            aba.append([
                data_liberacao.strftime("%d/%m/%Y %H:%M:%S") if data_liberacao else "",
                registro["usuario"],
                registro["perfil"],
                registro["cpf_cliente"],
                registro["numero_ticket"],
                registro["id_transacao"],
                registro["id_garagem"],
                registro["resultado"],
                registro["mensagem"]
            ])

        buffer = io.BytesIO()
        planilha.save(buffer)
        buffer.seek(0)

        return buffer
