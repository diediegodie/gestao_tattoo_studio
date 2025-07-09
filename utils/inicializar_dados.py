#!/usr/bin/env python3
"""
Script de inicialização para criar todos os arquivos JSON necessários
para o funcionamento do sistema de gestão de estúdio de tatuagem.
"""

import json
from pathlib import Path

def criar_arquivo_json(caminho, conteudo_padrao):
    """Cria um arquivo JSON se não existir."""
    caminho = Path(caminho)
    
    # Cria o diretório se não existir
    caminho.parent.mkdir(parents=True, exist_ok=True)
    
    # Cria o arquivo se não existir
    if not caminho.exists():
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(conteudo_padrao, f, indent=4, ensure_ascii=False)
        print(f"✅ Arquivo criado: {caminho}")
    else:
        print(f"ℹ️  Arquivo já existe: {caminho}")

def inicializar_dados():
    """Inicializa todos os arquivos JSON necessários."""
    base_dir = Path(__file__).parent / "dados"
    
    # Lista de arquivos JSON necessários
    arquivos = {
        base_dir / "sessoes.json": {
            "sessoes_ativas": [],
            "historico": []
        },
        base_dir / "pagamentos.json": [],
        base_dir / "produtos.json": [],
        base_dir / "despesas.json": [],
        base_dir / "comissoes.json": []
    }
    
    print("🚀 Inicializando arquivos de dados...")
    
    for caminho, conteudo in arquivos.items():
        criar_arquivo_json(caminho, conteudo)
    
    print("✅ Inicialização concluída!")

if __name__ == "__main__":
    inicializar_dados() 