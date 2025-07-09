"""
Utilitários para leitura segura de arquivos JSON
com detecção automática de codificação
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Union

def ler_json_seguro(caminho: Path, padrao: Union[Dict, List] = None) -> Union[Dict, List]:
    """
    Lê um arquivo JSON de forma segura, tentando diferentes codificações.
    """
    if padrao is None:
        padrao = {}
    if not caminho.exists():
        return padrao
    codificacoes = ['utf-8', 'utf-8-sig']
    for codificacao in codificacoes:
        try:
            with open(caminho, 'r', encoding=codificacao) as f:
                return json.load(f)
        except UnicodeDecodeError:
            continue
        except json.JSONDecodeError:
            continue
        except Exception:
            continue
    return padrao

def salvar_json_seguro(caminho: Path, dados: Union[Dict, List]) -> bool:
    """
    Salva dados em um arquivo JSON de forma segura.
    
    Args:
        caminho: Caminho para o arquivo JSON
        dados: Dados a serem salvos
    
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        # Garante que o diretório existe
        caminho.parent.mkdir(parents=True, exist_ok=True)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo JSON {caminho}: {e}")
        return False

def corrigir_arquivo_json(caminho: Path, estrutura_padrao: Union[Dict, List] = {}) -> bool:
    """
    Corrige um arquivo JSON corrompido ou com codificação incorreta.
    
    Args:
        caminho: Caminho para o arquivo JSON
        estrutura_padrao: Estrutura padrão para o arquivo
    
    Returns:
        True se corrigiu com sucesso, False caso contrário
    """
    try:
        # Tenta ler o arquivo atual
        dados_atuais = ler_json_seguro(caminho, estrutura_padrao)
        
        # Salva com codificação correta
        return salvar_json_seguro(caminho, dados_atuais)
    except Exception as e:
        print(f"Erro ao corrigir arquivo JSON {caminho}: {e}")
        return False 