import hashlib
import logging

from backend.config import Config
from integrations.wps_service import WpsIntegrationService
from repository.auditoria_repository import AuditoriaRepository
from repository.cupom_repository import CupomRepository

logger = logging.getLogger(__name__)


class CupomService:

    def __init__(self):
        self.repository = CupomRepository()
        self.auditoria_repository = AuditoriaRepository()
        self.wps_integration = WpsIntegrationService()

    def log_transacao(self, correlation_id, mensagem, *args):
         logger.info(
             "[TRANSACAO:%s] " + mensagem,
             correlation_id,
             *args
            )

    def buscar_cupom(self, usuario_id, cpf):

        logger.info("Consultando CPF %s", cpf)

        resultado = self.repository.buscar_cupom(cpf)

        if resultado:
            status = "SUCESSO"
            mensagem = "Cupom encontrado."
            cupom_id = resultado["redeem_coupon_id"]
            logger.info("Cupom encontrado para o CPF %s", cpf)
        else:
            status = "NAO_ENCONTRADO"
            mensagem = "Nenhum cupom encontrado."
            cupom_id = None
            logger.info("Cupom não encontrado para o CPF %s", cpf)

        logger.info("Registrando auditoria da consulta de CPF %s", cpf)

        self.auditoria_repository.registrar(
            usuario_id=usuario_id,
            tipo_acao="BUSCA_CPF",
            cpf_cliente=cpf,
            numero_ticket="",
            id_transacao=None,
            cupom_id=cupom_id,
            resultado=status,
            mensagem=mensagem
        )

        return resultado

    def liberar_ticket(self, usuario_id, cpf, numero_ticket):

        logger.info("Iniciando liberação do ticket %s para CPF %s", numero_ticket, cpf)

        cupom = self.repository.buscar_cupom(cpf)

        logger.info("CPF recebido no backend: %s", repr(cpf))
        logger.info("Resultado buscar_cupom: %s", cupom)

        if not cupom or cupom["has_used"]:

            mensagem = "Ticket não encontrado ou já utilizado."

            logger.info("Cupom inválido para CPF %s: %s", cpf, mensagem)

            self.auditoria_repository.registrar(
                usuario_id=usuario_id,
                tipo_acao="LIBERACAO_TICKET",
                cpf_cliente=cpf,
                numero_ticket=numero_ticket,
                id_transacao=None,
                cupom_id=None,
                resultado="CUPOM_INVALIDO",
                mensagem=mensagem,
                id_garagem=Config.WPS_ID_GARAGEM
            )

            return {
                "sucesso": False,
                "mensagem": mensagem
            }

        id_transacao = self.repository.obter_proximo_id_transacao()

        codigo_seguranca = self.gerar_codigo_seguranca(numero_ticket, id_transacao)

        payload = self.montar_payload_wps(numero_ticket, id_transacao, codigo_seguranca)

        self.log_transacao(
          id_transacao,
          "Enviando requisição para WPS"
        )

        resposta_wps = self.wps_integration.enviar_liberacao(payload, codigo_seguranca, id_transacao)

        self.log_transacao(
          id_transacao,
          "Resposta WPS: %s",
           resposta_wps
        )

        if resposta_wps.sucesso:

            self.log_transacao(
                id_transacao,
                "Atualizando cupom %s como utilizado (usuário %s)",
                cupom["redeem_coupon_id"],
                cupom["user_id"]
            )

            self.repository.atualizar_cupom_utilizado(
                cupom["redeem_coupon_id"],
                cupom["user_id"]
            )

            status_auditoria = "SUCESSO"

        elif resposta_wps.status_http is None:

            status_auditoria = "TIMEOUT" if "Timeout" in resposta_wps.mensagem else "ERRO_COMUNICACAO"

        else:

            status_auditoria = f"ERRO_HTTP_{resposta_wps.status_http}"

        self.log_transacao(
         id_transacao,
         "Registrando auditoria da liberação do ticket %s",
         numero_ticket
        )

        self.auditoria_repository.registrar(
            usuario_id=usuario_id,
            tipo_acao="LIBERACAO_TICKET",
            cpf_cliente=cpf,
            numero_ticket=numero_ticket,
            id_transacao=id_transacao,
            cupom_id=cupom["redeem_coupon_id"],
            resultado=status_auditoria,
            mensagem=resposta_wps.mensagem,
            id_garagem=Config.WPS_ID_GARAGEM
        )

        return {
            "sucesso": resposta_wps.sucesso,
            "mensagem": resposta_wps.mensagem
        }

    def gerar_codigo_seguranca(self, numero_ticket, id_transacao):

        base = (
            f"{numero_ticket}"
            f"{Config.WPS_UDID}"
            f"{Config.WPS_IP}"
            f"{Config.WPS_BANDEIRA}"
            f"{Config.WPS_PORTADOR}"
            f"{id_transacao}"
            f"{Config.WPS_SECRET_KEY}"
        )

        return hashlib.sha1(base.encode("utf-8")).hexdigest()

    def montar_payload_wps(self, numero_ticket, id_transacao, codigo_seguranca):

        return {
            "udid": Config.WPS_UDID,
            "numeroTicket": numero_ticket,
            "codigoDeSeguranca": codigo_seguranca,
            "valor": 0,
            "enderecoIp": Config.WPS_IP,
            "bandeira": Config.WPS_BANDEIRA,
            "cartaoDeCredito": Config.WPS_CARTAO,
            "portador": Config.WPS_PORTADOR,
            "validade": Config.WPS_VALIDADE,
            "idTransacao": id_transacao,
            "criptografarCartao": True,
            "idPromocao": Config.WPS_ID_PROMOCAO,
            "idGaragem": Config.WPS_ID_GARAGEM
        }
