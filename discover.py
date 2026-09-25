"""
Descoberta de oportunidades.

Este módulo é o ponto de extensão principal: cada função 'buscar_*'
representa uma fonte de oportunidades. Comece com UMA fonte real e
validada manualmente por você antes de automatizar a próxima.

IMPORTANTE: nenhuma função aqui deve criar contas, aceitar termos de
uso ou se cadastrar em nome do usuário. Isso precisa ser feito por
você, uma única vez, manualmente — depois disso o agente usa a API
da conta já existente.
"""


def buscar_oportunidades() -> list[dict]:
    """
    Ponto único de entrada chamado pelo orquestrador.
    Agrega o resultado de todas as fontes habilitadas.

    Retorna lista de dicts no formato:
    {
        "nome": str,
        "categoria": str,
        "capital_necessario": float | None,
        "receita_potencial": float | None,
        "custo_estimado": float | None,
        "tempo_estimado_horas": float | None,
        "risco": "baixo" | "medio" | "alto",
        "grau_automacao": "total" | "parcial" | "manual",
        "escalabilidade": "baixa" | "media" | "alta",
        "dependencia_terceiros": str,
        "confianca_estimativa": "dado_real" | "incerto",
    }
    """
    oportunidades = []
    # Exemplo de fonte (desativada até você configurar uma API real):
    # oportunidades += buscar_via_fonte_x()
    return oportunidades


# --- Esqueleto de fonte real, a ativar quando você tiver uma API/conta ---
# def buscar_via_fonte_x() -> list[dict]:
#     import requests
#     resposta = requests.get("https://api-real.exemplo.com/dados", timeout=20)
#     dados = resposta.json()
#     return [
#         {
#             "nome": item["titulo"],
#             "categoria": "exemplo",
#             "capital_necessario": None,
#             "receita_potencial": None,
#             "custo_estimado": None,
#             "tempo_estimado_horas": None,
#             "risco": "medio",
#             "grau_automacao": "parcial",
#             "escalabilidade": "media",
#             "dependencia_terceiros": "API externa",
#             "confianca_estimativa": "incerto",
#         }
#         for item in dados
#     ]
