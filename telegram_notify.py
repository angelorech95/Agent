"""
Envia mensagens para você via Telegram.
Também é usado para ler o comando /stop enviado por você.
"""
import requests
from core.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def enviar(mensagem: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[telegram desativado] {mensagem}")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(
            url,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"},
            timeout=15,
        )
    except Exception as e:
        print(f"[erro ao notificar telegram] {e}")


def checar_comando_stop() -> bool:
    """
    Verifica as últimas mensagens enviadas ao bot procurando por '/stop'.
    Retorna True se o comando STOP foi recebido.
    """
    if not TELEGRAM_BOT_TOKEN:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    try:
        r = requests.get(url, timeout=15, params={"limit": 5, "offset": -5})
        r.raise_for_status()
        updates = r.json().get("result", [])
        for u in updates:
            texto = u.get("message", {}).get("text", "")
            if texto.strip().lower() == "/stop":
                return True
    except Exception as e:
        print(f"[erro ao checar stop] {e}")
    return False
