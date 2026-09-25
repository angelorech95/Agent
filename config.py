"""
Configuração central do agente.
Todas as credenciais vêm de variáveis de ambiente (GitHub Actions Secrets).
Nunca coloque chaves reais neste arquivo.
"""
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Ações que o agente tem permissão de executar sozinho.
# Adicione aqui SOMENTE ações já validadas manualmente por você
# (conta criada, API testada, termos de uso lidos).
ACOES_PERMITIDAS = {
    # "publicar_conteudo_blog": True,
    # "enviar_relatorio_afiliado": True,
}

CICLO_MAX_DECISOES_LOG = 200
