import json
import os
from datetime import datetime

CAMINHO_ARQUIVO = "dados/sessoes.json"

def carregar_agendamentos():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            
            if isinstance(dados, list):  # Compatibilidade com versão antiga
                novos_dados = {"sessoes_ativas": dados, "historico": []}
                with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
                    json.dump(novos_dados, arquivo, indent=4, ensure_ascii=False)
                return dados
            
            return dados.get("sessoes_ativas", [])
            
    except (json.JSONDecodeError, IOError):
        return []

def salvar_agendamentos(lista):
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {"sessoes_ativas": [], "historico": []}
    
    dados["sessoes_ativas"] = lista
    
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# ... (mantenha o restante das funções existentes sem alterações)

def gerar_novo_id(agendamentos):
    if not agendamentos:
        return 1
    return max(s["id"] for s in agendamentos) + 1


def agendar_sessao(cliente, artista, data, hora, valor=None, observacoes=""):
    try:
        datetime.strptime(data, "%Y-%m-%d")
        datetime.strptime(hora, "%H:%M")
    except ValueError:
        print("Data ou hora em formato inválido.")
        return

    agendamentos = carregar_agendamentos()
    nova_sessao = {
        "id": gerar_novo_id(agendamentos),
        "cliente": cliente,
        "artista": artista,
        "data": data,
        "hora": hora,
        "valor": float(valor) if valor else None,
        "observacoes": observacoes,
        "paga": False  # Adicione esta linha
    }
    agendamentos.append(nova_sessao)
    salvar_agendamentos(agendamentos)
    print("Sessão agendada com sucesso.")

def excluir_agendamento(indice):
    agendamentos = carregar_agendamentos()
    if 0 <= indice < len(agendamentos):
        agendamentos.pop(indice)
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(agendamentos, f, indent=4, ensure_ascii=False)
