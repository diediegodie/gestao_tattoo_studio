import json
import os
from pathlib import Path

CAMINHO_ARQUIVO = Path(__file__).parent.parent / "dados" / "produtos.json"

# --- Função para carregar os produtos do arquivo JSON ---
def carregar_produtos():
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
def cadastrar_produto(nome, descricao, quantidade):
    produtos = carregar_produtos()
    
    # Verifica se já existe produto com mesmo nome (case insensitive)
    if any(p["nome"].lower() == nome.lower() for p in produtos):
        return False  # Produto já existe, não cadastra de novo

    novo = {
        "id": gerar_novo_id(produtos),
        "nome": nome,
        "descricao": descricao,
        "quantidade": quantidade,
    }

    produtos.append(novo)
    salvar_produtos(produtos)
    return True


# --- Excluir produto pelo nome ---
def excluir_produto(nome):
    produtos = carregar_produtos()
    produtos_filtrados = [p for p in produtos if p["nome"] != nome]
    salvar_produtos(produtos_filtrados)
