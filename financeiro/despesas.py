import json
import os
from datetime import datetime

CAMINHO_ARQUIVO = "dados/despesas.json"

def carregar_despesas():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []

def salvar_despesas(lista):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, indent=4, ensure_ascii=False)

def registrar_despesa(valor, categoria, descricao):
    despesas = carregar_despesas()
    nova_despesa = {
        "data": datetime.now().strftime("%Y-%m-%d"),
        "valor": float(valor),
        "categoria": categoria.lower(),
        "descricao": descricao
    }
    despesas.append(nova_despesa)
    salvar_despesas(despesas)
    print("Despesa registrada com sucesso.")

def gerar_relatorio(tipo="diario"):
    despesas = carregar_despesas()
    hoje = datetime.now().date()

    total = 0.0
    print(f"\n📉 RELATÓRIO DE DESPESAS {tipo.upper()}:\n")

    for despesa in despesas:
        data_despesa = datetime.strptime(despesa["data"], "%Y-%m-%d").date()

        if tipo == "diario" and data_despesa == hoje:
            mostrar_e_acumular(despesa, total)
            total += despesa["valor"]

        elif tipo == "semanal" and (hoje - data_despesa).days <= 7:
            mostrar_e_acumular(despesa, total)
            total += despesa["valor"]

        elif tipo == "mensal" and data_despesa.month == hoje.month and data_despesa.year == hoje.year:
            mostrar_e_acumular(despesa, total)
            total += despesa["valor"]

    print(f"\n➡ Total despesas {tipo}: R$ {total:.2f}\n")

def mostrar_e_acumular(despesa, _):
    print(f"{despesa['data']} | R$ {despesa['valor']:.2f} | {despesa['categoria']} | {despesa['descricao']}")
