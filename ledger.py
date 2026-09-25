"""
Controle de contadores diários da carteira (gasto_hoje, perda_acumulada_hoje).
Chamado automaticamente no início do ciclo quando a data mudou.
"""
from datetime import date
from core import db


def resetar_contadores_diarios_se_necessario():
    carteira = db.select("carteira", {"order": "id.desc", "limit": "1"})[0]
    hoje = date.today().isoformat()

    if str(carteira.get("data_referencia")) != hoje:
        db.update(
            "carteira",
            {"id": f"eq.{carteira['id']}"},
            {"gasto_hoje": 0, "perda_acumulada_hoje": 0, "data_referencia": hoje},
        )
