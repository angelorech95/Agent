-- ============================================================
-- Schema do Agente Autônomo de Geração de Receita
-- Rodar isto uma vez no editor SQL do painel Supabase
-- ============================================================

CREATE TABLE IF NOT EXISTS config (
    chave TEXT PRIMARY KEY,
    valor TEXT,
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

-- Kill switch. status = 'RUNNING' ou 'STOPPED'
INSERT INTO config (chave, valor) VALUES ('status', 'RUNNING')
ON CONFLICT (chave) DO NOTHING;

CREATE TABLE IF NOT EXISTS carteira (
    id SERIAL PRIMARY KEY,
    saldo_disponivel NUMERIC NOT NULL DEFAULT 0,
    capital_reservado NUMERIC NOT NULL DEFAULT 0,
    limite_max_operacao NUMERIC NOT NULL DEFAULT 10,
    limite_max_diario NUMERIC NOT NULL DEFAULT 30,
    limite_max_perda NUMERIC NOT NULL DEFAULT 50,
    perda_acumulada_hoje NUMERIC NOT NULL DEFAULT 0,
    gasto_hoje NUMERIC NOT NULL DEFAULT 0,
    data_referencia DATE DEFAULT CURRENT_DATE,
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

INSERT INTO carteira (saldo_disponivel, limite_max_operacao, limite_max_diario, limite_max_perda)
SELECT 0, 10, 30, 50
WHERE NOT EXISTS (SELECT 1 FROM carteira);

CREATE TABLE IF NOT EXISTS oportunidades (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT,
    capital_necessario NUMERIC,
    receita_potencial NUMERIC,
    custo_estimado NUMERIC,
    margem_estimada NUMERIC,
    tempo_estimado_horas NUMERIC,
    risco TEXT,
    grau_automacao TEXT,
    escalabilidade TEXT,
    dependencia_terceiros TEXT,
    confianca_estimativa TEXT DEFAULT 'incerto',
    status TEXT DEFAULT 'descoberta',
    criado_em TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transacoes (
    id SERIAL PRIMARY KEY,
    oportunidade_id INT REFERENCES oportunidades(id),
    tipo TEXT NOT NULL,          -- 'receita' ou 'custo'
    valor NUMERIC NOT NULL,
    status TEXT NOT NULL,        -- 'executada' | 'bloqueada' | 'erro'
    motivo_bloqueio TEXT,
    criado_em TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS decisoes_log (
    id SERIAL PRIMARY KEY,
    ciclo_id TEXT,
    etapa TEXT,
    detalhe JSONB,
    criado_em TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS heartbeat (
    id SERIAL PRIMARY KEY,
    ciclo_id TEXT,
    executado_em TIMESTAMPTZ DEFAULT now()
);
