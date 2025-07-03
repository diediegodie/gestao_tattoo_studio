import json
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
CAMINHO_ARQUIVO = BASE_DIR / "cadastro_interno" / "dados" / "artistas.json"

def carregar_artistas():
    try:
        if not CAMINHO_ARQUIVO.exists():
            CAMINHO_ARQUIVO.parent.mkdir(exist_ok=True)
            with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []
        
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados if isinstance(dados, list) else []
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erro ao carregar artistas: {str(e)}")
        return []

def salvar_artistas(lista):
    try:
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar artistas: {str(e)}")
        return False

def adicionar_artista(nome):
    if not nome or not isinstance(nome, str):
        return False
        
    artistas = carregar_artistas()
    nome_formatado = nome.strip().title()
    
    if nome_formatado and nome_formatado not in artistas:
        artistas.append(nome_formatado)
        return salvar_artistas(artistas)
    return False
