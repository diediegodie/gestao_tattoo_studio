import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CAMINHO_PAGAMENTOS = BASE_DIR / "dados" / "pagamentos.json"

def carregar_pagamentos():
    try:
        with open(CAMINHO_PAGAMENTOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_pagamentos(pagamentos):
    try:
        with open(CAMINHO_PAGAMENTOS, "w", encoding="utf-8") as arquivo:
            json.dump(pagamentos, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar pagamentos: {e}")
        return False

def registrar_pagamento(novo_pagamento):
    pagamentos = carregar_pagamentos()
    pagamentos.append(novo_pagamento)
    return salvar_pagamentos(pagamentos)

def excluir_pagamento(indice):
    pagamentos = carregar_pagamentos()
    if 0 <= indice < len(pagamentos):
        pagamentos.pop(indice)
        return salvar_pagamentos(pagamentos)
    return False

def gerar_extrato_mensal(mes, ano):
    pagamentos = carregar_pagamentos()
    extrato = []
    total_mes = 0.0

    for pagamento in pagamentos:
        try:
            data_pagamento = datetime.strptime(pagamento["data"], "%Y-%m-%d").date()
            if data_pagamento.month == mes and data_pagamento.year == ano:
                valor = float(pagamento.get("valor", 0))
                comissao = valor * 0.7  # 70% para o artista
                
                pagamento_formatado = {
                    "data": pagamento.get("data", ""),
                    "cliente": pagamento.get("cliente", ""),
                    "artista": pagamento.get("artista", ""),
                    "valor": valor,
                    "comissao": comissao,
                    "forma_pagamento": pagamento.get("forma_pagamento", "Não informado"),
                    "descricao": pagamento.get("descricao", "")
                }
                extrato.append(pagamento_formatado)
                total_mes += valor
        except (KeyError, ValueError):
            continue

    hoje = datetime.now().date()
    if mes == hoje.month and ano == hoje.year:
        return {"extrato": extrato, "total": total_mes, "completo": False}
    
    return {"extrato": extrato, "total": total_mes, "completo": True}

def gerar_relatorio(tipo="mensal"):
    pagamentos = carregar_pagamentos()
    hoje = datetime.now().date()
    relatorio = {
        "detalhes": [],
        "totais": {
            "valor_total": 0.0,
            "comissao_total": 0.0,
            "quantidade": 0
        }
    }

    for pagamento in pagamentos:
        try:
            data_pagamento = datetime.strptime(pagamento["data"], "%Y-%m-%d").date()
            incluir = False

            if tipo == "diario" and data_pagamento == hoje:
                incluir = True
            elif tipo == "semanal" and (hoje - data_pagamento).days <= 7:
                incluir = True
            elif tipo == "mensal" and data_pagamento.month == hoje.month and data_pagamento.year == hoje.year:
                incluir = True

            if incluir:
                valor = float(pagamento.get("valor", 0))
                # Usa a comissão salva se existir, senão calcula 30%
                comissao_salva = pagamento.get("valor_comissao", 0)
                if comissao_salva > 0:
                    comissao = float(comissao_salva)
                else:
                    comissao = valor * 0.7
                
                relatorio["detalhes"].append({
                    "data": pagamento.get("data", ""),
                    "cliente": pagamento.get("cliente", ""),
                    "artista": pagamento.get("artista", ""),
                    "valor": valor,
                    "comissao": comissao,
                    "forma_pagamento": pagamento.get("forma_pagamento", "Não informado"),
                    "descricao": pagamento.get("descricao", "")
                })
                
                relatorio["totais"]["valor_total"] += valor
                relatorio["totais"]["comissao_total"] += comissao
                relatorio["totais"]["quantidade"] += 1

        except (KeyError, ValueError) as e:
            print(f"Erro ao processar pagamento: {e}")

    return relatorio


def mostrar_e_acumular(pagamento, _):
    print(
        f"{pagamento['data']} | {pagamento['cliente']} | R$ {pagamento['valor']:.2f} | {pagamento['forma_pagamento']} | {pagamento['descricao']}"
    )
