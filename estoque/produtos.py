import json
import os

CAMINHO_ARQUIVO = "dados/produtos.json"

# --- Função para carregar os produtos do arquivo JSON ---
def carregar_produtos():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []

# --- Função para salvar lista de produtos no JSON ---
def salvar_produtos(lista):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, indent=4, ensure_ascii=False)

# --- Gerar novo ID incremental (opcional) ---
def gerar_novo_id(produtos):
    if not produtos:
        return 1
    return max(p.get("id", 0) for p in produtos) + 1

# --- Cadastrar novo produto ---
def cadastrar_produto(nome, descricao, valor_unitario, quantidade, total):
    produtos = carregar_produtos()

    novo = {
        "id": gerar_novo_id(produtos),
        "nome": nome,
        "descricao": descricao,
        "valor_unitario": valor_unitario,
        "quantidade": quantidade,
        "total": total,
    }

    produtos.append(novo)
    salvar_produtos(produtos)

# --- Excluir produto pelo nome ---
def excluir_produto(nome):
    produtos = carregar_produtos()
    produtos_filtrados = [p for p in produtos if p["nome"] != nome]
    salvar_produtos(produtos_filtrados)
