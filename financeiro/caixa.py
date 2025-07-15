import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CAMINHO_PAGAMENTOS = BASE_DIR / "dados" / "pagamentos.json"


def carregar_pagamentos():
    if not CAMINHO_PAGAMENTOS.exists():
        CAMINHO_PAGAMENTOS.parent.mkdir(exist_ok=True)
        with open(CAMINHO_PAGAMENTOS, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo)
        return []
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
    """
    Para meses anteriores, lê dos arquivos de backup. Para o mês atual, lê do arquivo principal.
    """
    from pathlib import Path
    import json

    base_dir = Path(__file__).parent.parent / "dados"
    backup_dir = base_dir / "historico_antigo"
    hoje = datetime.now().date()
    extrato = []
    total_mes = 0.0

    pagamentos_arquivados = []
    pagamentos = []
    if mes == hoje.month and ano == hoje.year:
        pagamentos = carregar_pagamentos()
    else:
        backup_pagamentos_path = backup_dir / f"pagamentos_{ano}_{mes:02d}.json"
        if backup_pagamentos_path.exists():
            with open(backup_pagamentos_path, "r", encoding="utf-8") as f:
                pagamentos_arquivados = json.load(f)
        else:
            pagamentos_arquivados = []

    # Extrato principal (pagamentos do mês atual)
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
                    "forma_pagamento": pagamento.get(
                        "forma_pagamento", "Não informado"
                    ),
                    "descricao": pagamento.get("descricao", ""),
                }
                extrato.append(pagamento_formatado)
                total_mes += valor
        except (KeyError, ValueError):
            continue

    # Pagamentos arquivados (para meses anteriores)
    pagamentos_arquivados_formatados = []
    for pagamento in pagamentos_arquivados:
        try:
            data_pagamento = datetime.strptime(pagamento["data"], "%Y-%m-%d").date()
            if data_pagamento.month == mes and data_pagamento.year == ano:
                valor = float(pagamento.get("valor", 0))
                pagamento_formatado = {
                    "data": pagamento.get("data", ""),
                    "cliente": pagamento.get("cliente", ""),
                    "artista": pagamento.get("artista", ""),
                    "valor": valor,
                    "forma_pagamento": pagamento.get(
                        "forma_pagamento", "Não informado"
                    ),
                    "descricao": pagamento.get("descricao", ""),
                }
                pagamentos_arquivados_formatados.append(pagamento_formatado)
        except (KeyError, ValueError):
            continue

    # Comissões
    comissoes = []
    total_comissoes = 0.0
    backup_comissoes_path = backup_dir / f"comissoes_{ano}_{mes:02d}.json"
    if backup_comissoes_path.exists():
        with open(backup_comissoes_path, "r", encoding="utf-8") as f:
            comissoes_data = json.load(f)
        for c in comissoes_data:
            try:
                data_comissao = datetime.strptime(c["data"], "%Y-%m-%d").date()
                if data_comissao.month == mes and data_comissao.year == ano:
                    valor_comissao = float(c.get("valor_comissao", 0))
                    valor_total = float(c.get("valor_total", 0))
                    comissao_formatada = {
                        "data": c.get("data", ""),
                        "cliente": c.get("cliente", ""),
                        "artista": c.get("artista", ""),
                        "valor_comissao": valor_comissao,
                        "valor_total": valor_total,
                        "descricao": c.get("descricao", ""),
                        "tipo": c.get("tipo", ""),
                    }
                    comissoes.append(comissao_formatada)
                    total_comissoes += valor_comissao
            except (KeyError, ValueError):
                continue

    # Sessões arquivadas
    sessoes_arquivadas = []
    backup_sessoes_path = backup_dir / f"sessoes_{ano}_{mes:02d}.json"
    if backup_sessoes_path.exists():
        with open(backup_sessoes_path, "r", encoding="utf-8") as f:
            sessoes_arquivadas = json.load(f)

    completo = not (mes == hoje.month and ano == hoje.year)
    return {
        "extrato": extrato,
        "total": total_mes,
        "completo": completo,
        "comissoes": comissoes,
        "total_comissoes": total_comissoes,
        "sessoes_arquivadas": sessoes_arquivadas,
        "pagamentos_arquivados": pagamentos_arquivados_formatados,
    }


def gerar_relatorio(tipo="mensal"):
    pagamentos = carregar_pagamentos()
    hoje = datetime.now().date()
    relatorio = {
        "detalhes": [],
        "totais": {"valor_total": 0.0, "comissao_total": 0.0, "quantidade": 0},
    }

    for pagamento in pagamentos:
        try:
            data_pagamento = datetime.strptime(pagamento["data"], "%Y-%m-%d").date()
            incluir = False

            if tipo == "diario" and data_pagamento == hoje:
                incluir = True
            elif tipo == "semanal" and (hoje - data_pagamento).days <= 7:
                incluir = True
            elif (
                tipo == "mensal"
                and data_pagamento.month == hoje.month
                and data_pagamento.year == hoje.year
            ):
                incluir = True

            if incluir:
                valor = float(pagamento.get("valor", 0))
                # Usa a comissão salva se existir, senão calcula 30%
                comissao_salva = pagamento.get("valor_comissao", 0)
                if comissao_salva > 0:
                    comissao = float(comissao_salva)
                else:
                    comissao = valor * 0.7

                relatorio["detalhes"].append(
                    {
                        "data": pagamento.get("data", ""),
                        "cliente": pagamento.get("cliente", ""),
                        "artista": pagamento.get("artista", ""),
                        "valor": valor,
                        "comissao": comissao,
                        "forma_pagamento": pagamento.get(
                            "forma_pagamento", "Não informado"
                        ),
                        "descricao": pagamento.get("descricao", ""),
                    }
                )

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
