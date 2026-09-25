"""
Motor de decisão. Pontua oportunidades e decide, sozinho, quais avançam.
Nenhuma etapa aqui pede confirmação humana.
"""

PESO_MARGEM = 0.4
PESO_RISCO = 0.3
PESO_AUTOMACAO = 0.2
PESO_ESCALABILIDADE = 0.1

MAPA_RISCO = {"baixo": 1.0, "medio": 0.5, "alto": 0.1}
MAPA_AUTOMACAO = {"total": 1.0, "parcial": 0.5, "manual": 0.0}
MAPA_ESCALA = {"alta": 1.0, "media": 0.5, "baixa": 0.2}


def pontuar(oportunidade: dict) -> float:
    receita = oportunidade.get("receita_potencial") or 0
    custo = oportunidade.get("custo_estimado") or 0
    margem = (receita - custo) if (receita and custo is not None) else 0

    # Oportunidades sem dado real pesam menos automaticamente —
    # nunca decide com base em número inventado.
    fator_confianca = 1.0 if oportunidade.get("confianca_estimativa") == "dado_real" else 0.3

    score = (
        PESO_MARGEM * min(margem / 100, 1.0)
        + PESO_RISCO * MAPA_RISCO.get(oportunidade.get("risco"), 0.3)
        + PESO_AUTOMACAO * MAPA_AUTOMACAO.get(oportunidade.get("grau_automacao"), 0.0)
        + PESO_ESCALABILIDADE * MAPA_ESCALA.get(oportunidade.get("escalabilidade"), 0.3)
    )
    return round(score * fator_confianca, 4)


def selecionar_melhores(oportunidades: list[dict], top_n: int = 3) -> list[dict]:
    ranqueadas = sorted(oportunidades, key=pontuar, reverse=True)
    return ranqueadas[:top_n]
