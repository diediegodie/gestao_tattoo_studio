import json
import os
from pathlib import Path
from estoque.produtos import carregar_produtos, salvar_produtos

CAMINHO_ARQUIVO = Path(__file__).parent.parent / "dados" / "sessoes.json"


def registrar_procedimento(id_agendamento, materiais_usados):
    agendamentos = carregar_agendamentos()
    produtos = carregar_produtos()
    custo_total = 0.0

    # Localiza o agendamento
    agendamento = next((s for s in agendamentos if s["id"] == id_agendamento), None)
    if not agendamento:
        print("Agendamento não encontrado.")
        return

    # Verifica, desconta do estoque e calcula o custo
    for item in materiais_usados:
        produto = next((p for p in produtos if p["id"] == item["id_produto"]), None)
        if not produto:
            print(f"Produto ID {item['id_produto']} não encontrado.")
            return

        if produto["quantidade_estoque"] < item["quantidade"]:
            print(f"Estoque insuficiente para {produto['nome']}.")
            return

        # Deduz do estoque
        produto["quantidade_estoque"] -= item["quantidade"]

        # Soma custo
        custo_total += item["quantidade"] * produto["custo_medio"]

    # Atualiza estoque
    salvar_produtos(produtos)

    # Registra o procedimento dentro do agendamento
    agendamento["materiais_utilizados"] = materiais_usados
    agendamento["custo_total"] = round(custo_total, 2)

    salvar_agendamentos(agendamentos)
    print("Procedimento registrado com sucesso.")


# Reutiliza funções existentes:
def carregar_agendamentos():
    if not CAMINHO_ARQUIVO.exists():
        CAMINHO_ARQUIVO.parent.mkdir(exist_ok=True)
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo)
        return []
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def salvar_agendamentos(lista):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, indent=4, ensure_ascii=False)
