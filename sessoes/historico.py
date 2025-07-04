import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CAMINHO_ARQUIVO = BASE_DIR / "dados" / "sessoes.json"

def mover_para_historico(sessao):
    try:
        # Carrega os dados existentes
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {"sessoes_ativas": [], "historico": []}
    
    # Verifica se a sessão já existe no histórico
    if not any(s.get("id") == sessao.get("id") for s in dados["historico"]):
        # Prepara os dados da sessão para o histórico
        sessao_historico = {
            **sessao,
            "paga": True,
            "data_fechamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Adiciona ao histórico
        dados["historico"].append(sessao_historico)
        
        # Salva os dados atualizados
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    
    with open("dados/sessoes.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        