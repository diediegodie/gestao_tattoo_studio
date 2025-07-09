import os
import json
from datetime import datetime, timedelta
from pathlib import Path


def realizar_backup_mensal():
    """
    Salva os pagamentos e comissões do mês atual em arquivos de backup,
    depois limpa os arquivos de dados para o novo mês.
    """
    base_dir = Path(__file__).parent.parent / "dados"
    backup_dir = base_dir / "historico_antigo"
    backup_dir.mkdir(parents=True, exist_ok=True)

    hoje = datetime.now().date()
    ano = hoje.year
    mes = hoje.month

    # Backup de pagamentos do mês atual
    pagamentos_path = base_dir / "historico_pagamentos.json"
    pagamentos_mes = []
    if pagamentos_path.exists():
        with open(pagamentos_path, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
        pagamentos_mes = [
            p
            for p in pagamentos
            if p.get("data")
            and datetime.strptime(p["data"], "%Y-%m-%d").year == ano
            and datetime.strptime(p["data"], "%Y-%m-%d").month == mes
        ]
        if pagamentos_mes:
            backup_pagamentos_path = backup_dir / f"pagamentos_{ano}_{mes:02d}.json"
            with open(backup_pagamentos_path, "w", encoding="utf-8") as f:
                json.dump(pagamentos_mes, f, indent=4, ensure_ascii=False)

    # Backup de comissões do mês atual
    comissoes_path = base_dir / "historico_comissoes.json"
    comissoes_mes = []
    if comissoes_path.exists():
        with open(comissoes_path, "r", encoding="utf-8") as f:
            comissoes = json.load(f)
        comissoes_mes = [
            c
            for c in comissoes
            if c.get("data")
            and datetime.strptime(c["data"], "%Y-%m-%d").year == ano
            and datetime.strptime(c["data"], "%Y-%m-%d").month == mes
        ]
        if comissoes_mes:
            backup_comissoes_path = backup_dir / f"comissoes_{ano}_{mes:02d}.json"
            with open(backup_comissoes_path, "w", encoding="utf-8") as f:
                json.dump(comissoes_mes, f, indent=4, ensure_ascii=False)

    # Limpa os arquivos de dados para o novo mês
    if pagamentos_path.exists():
        with open(pagamentos_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
    if comissoes_path.exists():
        with open(comissoes_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
