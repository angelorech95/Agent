"""
Camada de acesso ao Supabase (Postgres via REST).
Usa apenas 'requests' para não depender de SDKs pesados no runner do GitHub Actions.
"""
import requests
from core.config import SUPABASE_URL, SUPABASE_KEY

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}


def _url(table: str) -> str:
    return f"{SUPABASE_URL}/rest/v1/{table}"


def select(table: str, params: dict | None = None) -> list[dict]:
    r = requests.get(_url(table), headers=HEADERS, params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()


def insert(table: str, rows: dict | list[dict]) -> list[dict]:
    r = requests.post(_url(table), headers=HEADERS, json=rows, timeout=30)
    r.raise_for_status()
    return r.json()


def update(table: str, params: dict, patch: dict) -> list[dict]:
    r = requests.patch(_url(table), headers=HEADERS, params=params, json=patch, timeout=30)
    r.raise_for_status()
    return r.json()


def get_config(chave: str, default: str | None = None) -> str | None:
    rows = select("config", {"chave": f"eq.{chave}", "select": "valor"})
    return rows[0]["valor"] if rows else default


def set_config(chave: str, valor: str):
    existing = select("config", {"chave": f"eq.{chave}"})
    if existing:
        update("config", {"chave": f"eq.{chave}"}, {"valor": valor})
    else:
        insert("config", {"chave": chave, "valor": valor})
