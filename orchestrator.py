"""
Orquestrador principal. Disparado a cada ciclo pelo GitHub Actions.
Roda 100% sozinho, do início ao fim, sem pedir confirmação humana.
A única forma de interromper é o comando /stop no Telegram (ou setar
config.status = 'STOPPED' direto no Supabase).
"""
import sys
import uuid
from datetime import datetime, timezone

from core import db
from finance.ledger import resetar_contadores_diarios_se_necessario
from core.decision import selecionar_melhores
from research.discover import buscar_oportunidades
from execution.executor import executar_oportunidade
from security.risk_engine import sistema_esta_parado, registrar_decisao
from monitoring.telegram_notify import enviar, checar_comando_stop


def rodar_ciclo():
    ciclo_id = str(uuid.uuid4())[:8]
    inicio = datetime.now(timezone.utc)

    # 1. Checagem de STOP é sempre o primeiro passo, sem exceção.
    if checar_comando_stop():
        db.set_config("status", "STOPPED")

    if sistema_esta_parado():
        print(f"[{ciclo_id}] Sistema em STOP. Encerrando sem executar nada.")
        registrar_decisao(ciclo_id, "abort_stop", {"motivo": "status=STOPPED"})
        return

    registrar_decisao(ciclo_id, "inicio_ciclo", {"hora": inicio.isoformat()})

    # 1b. Resetar contadores diários automaticamente se a data virou.
    resetar_contadores_diarios_se_necessario()

    # 2. Pesquisar oportunidades novas.
    oportunidades = buscar_oportunidades()
    registrar_decisao(ciclo_id, "oportunidades_encontradas", {"total": len(oportunidades)})

    if not oportunidades:
        print(f"[{ciclo_id}] Nenhuma oportunidade nova encontrada.")
        db.insert("heartbeat", {"ciclo_id": ciclo_id})
        return

    # 3. Persistir oportunidades descobertas.
    salvas = db.insert("oportunidades", [
        {**o, "status": "avaliada"} for o in oportunidades
    ])

    # 4. Selecionar as melhores automaticamente.
    melhores = selecionar_melhores(salvas, top_n=3)
    registrar_decisao(ciclo_id, "selecionadas", {"nomes": [o["nome"] for o in melhores]})

    # 5. Executar automaticamente (sem aprovação manual) — bloqueado
    #    apenas pelos limites automáticos do risk_engine.
    resultados = []
    for oportunidade in melhores:
        resultado = executar_oportunidade(oportunidade, ciclo_id)
        resultados.append((oportunidade["nome"], resultado["status"]))

    # 6. Heartbeat — prova de que o ciclo rodou.
    db.insert("heartbeat", {"ciclo_id": ciclo_id})

    # 7. Notificação resumida (não obrigatória a cada ciclo, mas útil).
    resumo = "\n".join(f"- {nome}: {status}" for nome, status in resultados)
    enviar(f"*Ciclo {ciclo_id} concluído*\n{resumo}")

    print(f"[{ciclo_id}] Ciclo concluído. {len(resultados)} ações processadas.")


if __name__ == "__main__":
    try:
        rodar_ciclo()
    except Exception as e:
        enviar(f"⚠️ *Erro não tratado no ciclo*: {e}")
        print(f"Erro fatal: {e}", file=sys.stderr)
        sys.exit(1)
