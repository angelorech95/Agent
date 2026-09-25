"""
Execução das ações. Chamado somente depois que risk_engine.pode_executar()
já aprovou automaticamente — não há segunda etapa de confirmação humana.

Adicione aqui uma função por ação real (ex.: publicar_conteudo,
enviar_relatorio_cliente) e registre a ação em core/config.ACOES_PERMITIDAS
somente depois de validar manualmente a conta/API na plataforma alvo.
"""
from core import db
from security.risk_engine import pode_executar, registrar_decisao


def executar_oportunidade(oportunidade: dict, ciclo_id: str):
    acao = oportunidade.get("acao", "sem_acao_definida")
    valor = float(oportunidade.get("custo_estimado") or 0)

    permitido, motivo = pode_executar(acao, valor, ciclo_id)
    registrar_decisao(ciclo_id, "avaliacao_execucao", {
        "oportunidade": oportunidade.get("nome"),
        "acao": acao,
        "valor": valor,
        "permitido": permitido,
        "motivo": motivo,
    })

    if not permitido:
        db.insert("transacoes", {
            "oportunidade_id": oportunidade.get("id"),
            "tipo": "custo",
            "valor": valor,
            "status": "bloqueada",
            "motivo_bloqueio": motivo,
        })
        return {"status": "bloqueada", "motivo": motivo}

    try:
        resultado = _despachar(acao, oportunidade)
        db.insert("transacoes", {
            "oportunidade_id": oportunidade.get("id"),
            "tipo": "custo",
            "valor": valor,
            "status": "executada",
        })
        return {"status": "executada", "resultado": resultado}
    except Exception as e:
        db.insert("transacoes", {
            "oportunidade_id": oportunidade.get("id"),
            "tipo": "custo",
            "valor": valor,
            "status": "erro",
            "motivo_bloqueio": str(e),
        })
        return {"status": "erro", "motivo": str(e)}


def _despachar(acao: str, oportunidade: dict):
    """
    Roteador de ações reais. Adicione um 'if acao == ...' por integração
    real que você configurar (com conta/API já criada manualmente).
    """
    raise NotImplementedError(
        f"Nenhuma integração real configurada ainda para a ação '{acao}'. "
        "Adicione a função de execução real em execution/executor.py."
    )
