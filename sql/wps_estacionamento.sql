-- Sequence responsável por gerar o idTransacao enviado à WPS.
-- Nunca implementar contador manual: sempre usar SELECT nextval('wps_id_transacao_seq').
CREATE SEQUENCE IF NOT EXISTS wps_id_transacao_seq
    INCREMENT BY 1
    START WITH 28052500;

-- Auditoria das tentativas de liberação de ticket (sucesso, erro ou timeout).
CREATE TABLE IF NOT EXISTS estacionamento_auditoria (
    id            SERIAL PRIMARY KEY,
    cpf           VARCHAR(14)  NOT NULL,
    numero_ticket VARCHAR(50)  NOT NULL,
    id_transacao  BIGINT       NOT NULL,
    data_hora     TIMESTAMP    NOT NULL DEFAULT NOW(),
    status        VARCHAR(30)  NOT NULL,
    mensagem      TEXT,
    resposta_wps  JSONB,
    operador      VARCHAR(100)
);
