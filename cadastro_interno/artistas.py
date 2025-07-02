import json
import os

CAMINHO_ARQUIVO = "cadastro_interno/artistas.json"

def carregar_artistas():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_artistas(lista):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

def adicionar_artista(nome):
    artistas = carregar_artistas()
    if nome and nome not in artistas:
        artistas.append(nome)
        salvar_artistas(artistas)
        return True
    return False
