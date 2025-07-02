import json
import os
from datetime import datetime

CAMINHO_ARQUIVO = "dados/caixa.json"


def carregar_pagamentos():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []


def salvar_pagamentos(lista):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, indent=4, ensure_ascii=False)


def registrar_pagamento(valor, forma_pagamento, cliente, descricao, artista):
    pagamentos = carregar_pagamentos()
    novo_pagamento = {
        "data": datetime.now().strftime("%Y-%m-%d"),
        "valor": float(valor),
        "forma_pagamento": forma_pagamento.lower(),
        "cliente": cliente,
        "descricao": descricao,
        "artista": artista,
    }
    pagamentos.append(novo_pagamento)
    salvar_pagamentos(pagamentos)
    print("Pagamento registrado com sucesso.")


def excluir_pagamento(indice):
    pagamentos = carregar_pagamentos()
    if 0 <= indice < len(pagamentos):
        pagamentos.pop(indice)
        salvar_pagamentos(pagamentos)


def gerar_relatorio(tipo="diario"):
    pagamentos = carregar_pagamentos()
    hoje = datetime.now().date()

    total = 0.0
    print(f"\n📊 RELATÓRIO {tipo.upper()}:\n")

    for pagamento in pagamentos:
        data_pagamento = datetime.strptime(pagamento["data"], "%Y-%m-%d").date()

        if tipo == "diario" and data_pagamento == hoje:
            total += pagamento["valor"]
            mostrar_e_acumular(pagamento, total)

        elif tipo == "semanal" and (hoje - data_pagamento).days <= 7:
            total += pagamento["valor"]
            mostrar_e_acumular(pagamento, total)

        elif (
            tipo == "mensal"
            and data_pagamento.month == hoje.month
            and data_pagamento.year == hoje.year
        ):
            total += pagamento["valor"]
            mostrar_e_acumular(pagamento, total)

    print(f"\n➡ Total {tipo}: R$ {total:.2f}\n")



def mostrar_e_acumular(pagamento, _):
    print(
        f"{pagamento['data']} | {pagamento['cliente']} | R$ {pagamento['valor']:.2f} | {pagamento['forma_pagamento']} | {pagamento['descricao']}"
    )
