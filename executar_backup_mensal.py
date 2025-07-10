import os
import shutil
import json
from datetime import datetime

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(BASE_DIR, "dados")
BACKUP_DIR = os.path.join(DADOS_DIR, "historico_antigo")

# Files to backup: (source filename, backup prefix)
FILES = [
    ("historico_pagamentos.json", "pagamentos"),
    ("historico_comissoes.json", "comissoes"),
    ("sessoes_realizadas.json", "sessoes"),
]


def main():
    # Create backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"[OK] Pasta de backup criada: {BACKUP_DIR}")
    else:
        print(f"[OK] Pasta de backup já existe: {BACKUP_DIR}")

    now = datetime.now()
    year = now.year
    month = now.month

    for filename, prefix in FILES:
        src = os.path.join(DADOS_DIR, filename)
        backup_name = f"{prefix}_{year}_{month:02d}.json"
        dst = os.path.join(BACKUP_DIR, backup_name)

        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                print(f"[OK] Backup de {filename} salvo como {backup_name}")
                # Clear the original file
                with open(src, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                print(f"[OK] {filename} limpo para o novo mês.")
            except Exception as e:
                print(f"[ERRO] Falha ao processar {filename}: {e}")
        else:
            print(f"[AVISO] Arquivo não encontrado: {filename}")


if __name__ == "__main__":
    main()
