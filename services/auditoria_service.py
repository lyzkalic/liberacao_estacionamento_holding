import io
import logging
from datetime import datetime
from typing import ClassVar

import openpyxl

from repository.auditoria_repository import AuditoriaRepository

logger = logging.getLogger(__name__)


class AuditoriaService:

    COLUNAS: ClassVar[list[str]] = [
        "Data/Hora",
        "Usuário",
        "Perfil",
        "CPF Cliente",
        "Número Ticket",
        "ID Transação",
        "ID Garagem",
        "Resultado",
        "Mensagem",
    ]

    def __init__(self):
        self.repository = AuditoriaRepository()

    def listar_historico(
        self,
        cpf=None,
        usuario=None,
        status=None,
        data_inicial=None,
        data_final=None,
    ):
        logger.info(
            "Listando histórico de auditoria (filtros: cpf=%s, usuario=%s, status=%s, data_inicial=%s, data_final=%s)",
            cpf,
            usuario,
            status,
            data_inicial,
            data_final,
        )

        return self.repository.listar_historico(
            cpf=cpf,
            usuario=usuario,
            status=status,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def exportar_historico(
        self,
        cpf=None,
        usuario=None,
        status=None,
        data_inicial=None,
        data_final=None,
    ):
        logger.info("Exportação do Excel iniciada")

        registros = self.repository.exportar_historico(
            cpf=cpf,
            usuario=usuario,
            status=status,
            data_inicial=data_inicial,
            data_final=data_final,
        )

        buffer = self.gerar_excel(registros)

        logger.info(
            "Exportação do Excel concluída (%s registros)", len(registros)
        )

        return buffer

    def gerar_excel(self, registros):
        planilha = openpyxl.Workbook()

        aba = planilha.active
        aba.title = "Auditoria"

        aba.append(self.COLUNAS)

        for registro in registros:
            data_raw = registro.get("data_liberacao") or registro.get("criado_em")
            data_formatada = ""

            if isinstance(data_raw, datetime):
                data_formatada = data_raw.strftime("%d/%m/%Y %H:%M:%S")
            elif isinstance(data_raw, str):
                try:
                    # Trata string ISO vinda do JSON da API (ex: 2026-08-27T12:00:00)
                    dt = datetime.fromisoformat(data_raw.replace("Z", "+00:00"))
                    data_formatada = dt.strftime("%d/%m/%Y %H:%M:%S")
                except ValueError:
                    data_formatada = data_raw

            aba.append([
                data_formatada,
                registro.get("usuario", ""),
                registro.get("perfil", ""),
                registro.get("cpf_cliente", ""),
                registro.get("numero_ticket", ""),
                registro.get("id_transacao", ""),
                registro.get("id_garagem", ""),
                registro.get("resultado", ""),
                registro.get("mensagem", ""),
            ])

        buffer = io.BytesIO()
        planilha.save(buffer)
        buffer.seek(0)

        return buffer