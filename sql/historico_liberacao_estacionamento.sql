-- Histórico de auditoria: consultas de CPF e liberações de ticket, com o usuário responsável.
CREATE TABLE IF NOT EXISTS historico_liberacao_estacionamento (
    id             SERIAL PRIMARY KEY,
    usuario_id     INTEGER      NOT NULL REFERENCES autenticacao_estacionamento(id),
    tipo_acao      VARCHAR(30)  NOT NULL,
    cpf_cliente    VARCHAR(14),
    numero_ticket  VARCHAR(50),
    cupom_id       UUID,
    id_transacao   BIGINT,
    id_garagem     INTEGER,
    resultado      VARCHAR(30),
    mensagem       TEXT,
    data_liberacao TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
