# Agente Autônomo de Geração de Receita

Sistema roda 100% sozinho, em ciclos, disparado pelo GitHub Actions.
Não há aprovação manual por transação — a segurança vem apenas dos
limites automáticos configurados na tabela `carteira`.

## Deploy pelo iPhone (sem computador)

### 1. GitHub
1. App **GitHub** (ou Safari) → criar conta → criar repositório **privado**.
2. Subir todos os arquivos deste projeto para o repositório (pelo app do GitHub,
   ou pelo editor web completo em `github.dev/SEU_USUARIO/SEU_REPO` no Safari).

### 2. Supabase (banco de dados)
1. Safari → supabase.com → criar conta → **New Project** (plano free).
2. Menu **SQL Editor** → colar o conteúdo de `schema.sql` → Run.
3. Menu **Project Settings → API** → copiar:
   - `Project URL` → vai virar o secret `SUPABASE_URL`
   - `service_role key` (ou `anon key`, se preferir dar menos permissão) → vira `SUPABASE_KEY`

### 3. Telegram (painel de controle)
1. No Telegram, conversar com **@BotFather** → `/newbot` → seguir instruções → copiar o **token**.
2. Enviar qualquer mensagem para o seu bot recém-criado.
3. Acessar `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates` pelo Safari →
   pegar o campo `chat.id` da resposta → esse é o `TELEGRAM_CHAT_ID`.

### 4. Configurar os Secrets no GitHub
No repositório: **Settings → Secrets and variables → Actions → New repository secret**.
Cadastrar:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### 5. Ativar
- Ir em **Actions** no repositório → habilitar workflows.
- O ciclo (`cycle.yml`) já roda sozinho a cada 20 minutos a partir daí.
- Para testar sem esperar: **Actions → Ciclo do Agente → Run workflow**.

## Como parar o agente a qualquer momento
- Enviar `/stop` para o seu bot no Telegram, **ou**
- No Supabase, editar a tabela `config`, linha `status`, valor para `STOPPED`.

## Antes de ligar qualquer ação com dinheiro real
1. Crie você mesmo (manualmente) a conta na plataforma de destino (afiliado, blog,
   marketplace, etc.) e leia os termos de uso quanto a automação.
2. Implemente a função real da ação em `execution/executor.py` (dentro de `_despachar`).
3. Adicione a chave da API dessa plataforma como um novo Secret no GitHub.
4. Libere a ação em `core/config.py`, dicionário `ACOES_PERMITIDAS`.
5. Ajuste os limites em `carteira` (Supabase) para valores pequenos antes de liberar.

Sem esse passo 2, o agente pesquisa, decide e registra tudo sozinho, mas
qualquer ação real cai em `NotImplementedError` — de propósito, para nunca
"inventar" uma execução contra uma plataforma que não foi de fato integrada.

## Estrutura
```
core/          orquestração, config, banco, motor de decisão
research/      descoberta de oportunidades (plugar fontes reais aqui)
finance/       controle de limites diários
execution/     execução real das ações permitidas
security/      motor de risco (limites automáticos) + kill switch
monitoring/    notificações e alertas via Telegram
schema.sql     schema do banco (rodar uma vez no Supabase)
orchestrator.py  ponto de entrada de cada ciclo
.github/workflows/  agendamento (cron) e keep-alive
```
