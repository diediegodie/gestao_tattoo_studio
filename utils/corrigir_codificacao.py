#!/usr/bin/env python3
"""
Script para corrigir a codificação do arquivo sessoes.json
e garantir que ele esteja em UTF-8 válido.
"""

import json
from pathlib import Path

def corrigir_codificacao_sessoes():
    """Corrige a codificação do arquivo sessoes.json"""
    caminho = Path(__file__).parent / "dados" / "sessoes.json"
    
    print(f"🔧 Corrigindo codificação do arquivo: {caminho}")
    
    # Estrutura padrão para o arquivo sessoes.json
    estrutura_padrao = {
        "sessoes_ativas": [],
        "historico": []
    }
    
    # Lista de codificações para tentar
    codificacoes = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    dados_lidos = None
    
    # Tenta ler com diferentes codificações
    for codificacao in codificacoes:
        try:
            if caminho.exists():
                with open(caminho, 'r', encoding=codificacao) as f:
                    dados_lidos = json.load(f)
                print(f"✅ Arquivo lido com sucesso usando codificação: {codificacao}")
                break
            else:
                print("⚠️  Arquivo não existe, será criado com estrutura padrão")
                dados_lidos = estrutura_padrao
                break
        except UnicodeDecodeError:
            print(f"❌ Falha com codificação: {codificacao}")
            continue
        except json.JSONDecodeError:
            print(f"❌ JSON inválido com codificação: {codificacao}")
            continue
        except Exception as e:
            print(f"❌ Erro inesperado com codificação {codificacao}: {e}")
            continue
    
    # Se não conseguiu ler, usa estrutura padrão
    if dados_lidos is None:
        print("⚠️  Não foi possível ler o arquivo, usando estrutura padrão")
        dados_lidos = estrutura_padrao
    
    # Garante que a estrutura está correta
    if not isinstance(dados_lidos, dict):
        dados_lidos = estrutura_padrao
    
    if "sessoes_ativas" not in dados_lidos:
        dados_lidos["sessoes_ativas"] = []
    
    if "historico" not in dados_lidos:
        dados_lidos["historico"] = []
    
    # Salva com codificação UTF-8 correta
    try:
        # Garante que o diretório existe
        caminho.parent.mkdir(parents=True, exist_ok=True)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados_lidos, f, indent=4, ensure_ascii=False)
        
        print("✅ Arquivo salvo com codificação UTF-8 correta")
        print(f"📊 Estrutura do arquivo:")
        print(f"   - Sessões ativas: {len(dados_lidos['sessoes_ativas'])}")
        print(f"   - Histórico: {len(dados_lidos['historico'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando correção de codificação...")
    sucesso = corrigir_codificacao_sessoes()
    
    if sucesso:
        print("🎉 Correção concluída com sucesso!")
    else:
        print("💥 Erro na correção!") 