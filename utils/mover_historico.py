#!/usr/bin/env python3
"""
Script para mover dados do mês anterior para o histórico antigo.
Este script deve ser executado no primeiro dia de cada mês.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from historico.routes import mover_dados_para_historico
from datetime import date

def main():
    print("=== MOVIMENTAÇÃO AUTOMÁTICA DE DADOS ===")
    print(f"Data atual: {date.today().strftime('%d/%m/%Y')}")
    
    try:
        mover_dados_para_historico()
        print("✅ Dados movidos com sucesso para o histórico antigo!")
        print("📁 Verifique a pasta 'dados/historico_antigo' para os arquivos criados.")
    except Exception as e:
        print(f"❌ Erro ao mover dados: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 