import logging
import json

import requests

from backend.config import Config
from models.response import WpsResponse


logger = logging.getLogger(__name__)


class WpsIntegrationService:


    def log_transacao(self, correlation_id, mensagem, *args):
        logger.info(
            "[TRANSACAO:%s] " + mensagem,
            correlation_id,
            *args
        )


    def enviar_liberacao(self, payload, codigo_seguranca, correlation_id):

        payload["codigoDeSeguranca"] = codigo_seguranca

        api_key = codigo_seguranca
        api_key_id = Config.WPS_API_KEY_ID

        url = (
            f"https://parebem.parkingplus.com.br/servicos/2/pagamento"
            f"?apiKey={api_key}&apiKeyId={api_key_id}"
        )


        logger.info("API KEY (Hash dinâmico) enviada na URL: %s", api_key)
        logger.info("API KEY ID: %s", api_key_id)
        logger.info("Código de segurança no JSON: %s", codigo_seguranca)


        try:

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }


            logger.info("--- [CONFERÊNCIA PAYLOAD WPS] ---")
            logger.info("Payload sendo enviado: %s", payload)


            curl_command = (
                f"curl -X POST "
                f"\"{url}\" "
                f"-H \"Content-Type: application/json\" "
                f"-d '{json.dumps(payload)}'"
            )


            logger.info("--- [CURL PARA TESTE MANUAL] ---")
            logger.info("\n%s\n", curl_command)
            logger.info("--------------------------------")


            resposta = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=Config.WPS_TIMEOUT
            )


        except requests.exceptions.Timeout:


            self.log_transacao(
                correlation_id,
                "Timeout na comunicação com a WPS"
            )


            return WpsResponse(
                sucesso=False,
                status_http=None,
                mensagem="Não foi possível concluir a liberação (tempo de resposta da WPS excedido). Tente novamente.",
                resposta=None
            )


        except requests.exceptions.RequestException as erro:


            self.log_transacao(
                correlation_id,
                "Falha de comunicação com a WPS: %s",
                erro
            )


            return WpsResponse(
                sucesso=False,
                status_http=None,
                mensagem="Não foi possível concluir a liberação (falha de comunicação com a WPS). Tente novamente.",
                resposta={
                    "detalhe_tecnico": str(erro)
                }
            )


        self.log_transacao(
            correlation_id,
            "Status HTTP WPS: %s",
            resposta.status_code
        )


        self.log_transacao(
            correlation_id,
            "Body WPS: %s",
            resposta.text
        )


        corpo_resposta = self._extrair_corpo(resposta)


        if resposta.status_code == 200:

            return WpsResponse(
                sucesso=True,
                status_http=200,
                mensagem="Liberação realizada com sucesso na WPS.",
                resposta=corpo_resposta
            )


        if resposta.status_code == 400:

            return WpsResponse(
                sucesso=False,
                status_http=400,
                mensagem="Não foi possível concluir a liberação (dados rejeitados pela WPS). Tente novamente ou acione o suporte.",
                resposta=corpo_resposta
            )


        if resposta.status_code == 500:

            return WpsResponse(
                sucesso=False,
                status_http=500,
                mensagem="Não foi possível concluir a liberação (erro interno na WPS). Tente novamente.",
                resposta=corpo_resposta
            )


        return WpsResponse(
            sucesso=False,
            status_http=resposta.status_code,
            mensagem="Não foi possível concluir a liberação (retorno inesperado da WPS). Tente novamente.",
            resposta=corpo_resposta
        )


    def _extrair_corpo(self, resposta):

        try:

            return resposta.json()

        except ValueError:

            return resposta.text
