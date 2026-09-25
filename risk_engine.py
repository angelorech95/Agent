"""
Motor de segurança. TODA ação passa por pode_executar() antes de rodar.
Isto é 100% automático — não pede confirmação humana — mas bloqueia
qualquer ação que viole os limites numéricos definidos na carteira.
"""
from core import db
from core.config import ACOES_PERMITIDAS


class BloqueioSeguranca(Exception):
    pass


def sistema_esta_parado() -> bool:
    status = db.get_config("status", "RUNNING")
    return status == "STOPPED"


def carregar_carteira() -> dict:
    rows = db.select("carteira", {"order": "id.desc", "limit": "1"})
    if not rows:
        raise BloqueioSeguranca("Carteira não inicializada no banco.")
    return rows[0]


def pode_executar(acao: str, valor: float, ciclo_id: str) -> tuple[bool, str]:
    """
    Retorna (permitido, motivo).
    Roda automaticamente, sem intervenção humana — a segurança vem
    inteiramente dos limites numéricos, não de aprovação manual.
    """
    if sistema_esta_parado():
        return False, "STOP ativo: sistema pausado manualmente."

    if acao not in ACOES_PERMITIDAS:
        return False, f"Ação '{acao}' não está na allowlist (ACOES_PERMITIDAS)."

    carteira = carregar_carteira()

    if valor > float(carteira["limite_max_operacao"]):
        return False, "Valor excede o limite máximo por operação."

    if float(carteira["gasto_hoje"]) + valor > float(carteira["limite_max_diario"]):
        return False, "Excederia o limite máximo diário."

    if float(carteira["perda_acumulada_hoje"]) >= float(carteira["limite_max_perda"]):
        return False, "Limite máximo de perda diária já atingido."

    if valor > float(carteira["saldo_disponivel"]):
        return False, "Saldo disponível insuficiente."

    return True, "ok"


def registrar_decisao(ciclo_id: str, etapa: str, detalhe: dict):
    db.insert("decisoes_log", {"ciclo_id": ciclo_id, "etapa": etapa, "detalhe": detalhe})
