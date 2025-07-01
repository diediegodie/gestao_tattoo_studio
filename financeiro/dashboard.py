from financeiro.caixa import carregar_pagamentos
from financeiro.despesas import carregar_despesas
from datetime import datetime
from collections import defaultdict

def gerar_dashboard():
    pagamentos = carregar_pagamentos()
    despesas = carregar_despesas()

    total_receitas = sum(p["valor"] for p in pagamentos)
    total_despesas = sum(d["valor"] for d in despesas)
    saldo = total_receitas - total_despesas

    print("\n📊 DASHBOARD FINANCEIRO 📊")
    print(f"Total de receitas:  R$ {total_receitas:.2f}")
    print(f"Total de despesas:  R$ {total_despesas:.2f}")
    print(f"Saldo atual:        R$ {saldo:.2f}")

    gerar_percentual_por_categoria(despesas)
    verificar_alerta_gastos(despesas)

def gerar_percentual_por_categoria(despesas):
    print("\n📌 Percentual de despesas por categoria:")

    totais = defaultdict(float)
    total_geral = 0.0

    for d in despesas:
        categoria = d["categoria"]
        valor = d["valor"]
        totais[categoria] += valor
        total_geral += valor

    for categoria, valor in totais.items():
        percentual = (valor / total_geral) * 100 if total_geral else 0
        print(f" - {categoria.capitalize()}: R$ {valor:.2f} ({percentual:.1f}%)")

def verificar_alerta_gastos(despesas):
    hoje = datetime.now()
    gastos_por_mes = defaultdict(float)

    for d in despesas:
        data = datetime.strptime(d["data"], "%Y-%m-%d")
        chave = f"{data.year}-{data.month:02}"
        gastos_por_mes[chave] += d["valor"]

    if not gastos_por_mes:
        return

    mes_atual = f"{hoje.year}-{hoje.month:02}"
    media = sum(gastos_por_mes.values()) / len(gastos_por_mes)
    gasto_mes_atual = gastos_por_mes.get(mes_atual, 0)

    print("\n🚨 Verificação de gastos:")

    if gasto_mes_atual > media * 1.2:
        print(f" - ALERTA: despesas deste mês (R$ {gasto_mes_atual:.2f}) estão acima da média histórica (R$ {media:.2f})")
    else:
        print(" - Despesas deste mês estão dentro da média.")
