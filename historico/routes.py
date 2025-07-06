from flask import render_template, request, jsonify
from historico import historico_bp
import json
from pathlib import Path
from financeiro.caixa import carregar_pagamentos
from datetime import datetime, date
import os

@historico_bp.route("/sessoes", methods=["GET", "POST"])
def historico_sessoes():
    if request.method == "POST":
        # Processar confirmação de fechamento de sessão
        pass
    
    # Carregar dados de sessões
    with open(Path(__file__).parent.parent / "dados" / "sessoes.json", 'r', encoding='utf-8') as f:
        dados = json.load(f)
        sessoes_historico = dados.get('historico', [])
    
    # Inverter a ordem para mostrar os mais recentes no topo
    sessoes_historico.reverse()
    
    # Carregar dados de pagamentos
    pagamentos = carregar_pagamentos()
    
    # Inverter a ordem dos pagamentos para mostrar os mais recentes no topo
    pagamentos.reverse()
    
    # Calcular comissões por artista
    comissoes_artistas = calcular_comissoes_por_artista(sessoes_historico)
    
    return render_template("historico/historico.html", 
                         sessoes_historico=sessoes_historico,
                         pagamentos=pagamentos,
                         comissoes_artistas=comissoes_artistas)

@historico_bp.route("/historicos-antigos")
def historicos_antigos():
    return render_template("historico/historicos_antigos.html")

@historico_bp.route("/pagamentos")
def historico_pagamentos():
    return render_template("historico/pagamentos.html")

@historico_bp.route("/extrato/dados/<mes_ano>")
def extrato_dados(mes_ano):
    """Retorna dados de pagamentos de um mês específico"""
    try:
        # Verificar se o mês é do mês atual ou anterior
        data_atual = date.today()
        mes_ano_atual = data_atual.strftime("%Y-%m")
        
        if mes_ano >= mes_ano_atual:
            # Mês atual ou futuro - buscar na página financeiro
            pagamentos = carregar_pagamentos()
            pagamentos_mes = [p for p in pagamentos if p.get('data', '').startswith(mes_ano)]
        else:
            # Mês anterior - buscar no histórico antigo
            pagamentos_mes = carregar_historico_antigo(mes_ano, 'pagamentos')
        
        return jsonify({
            'success': True,
            'extrato': pagamentos_mes
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@historico_bp.route("/extrato/comissoes/<mes_ano>")
def extrato_comissoes(mes_ano):
    """Retorna dados de comissões de um mês específico"""
    try:
        # Verificar se o mês é do mês atual ou anterior
        data_atual = date.today()
        mes_ano_atual = data_atual.strftime("%Y-%m")
        
        if mes_ano >= mes_ano_atual:
            # Mês atual ou futuro - buscar na página de sessões
            with open(Path(__file__).parent.parent / "dados" / "sessoes.json", 'r', encoding='utf-8') as f:
                dados = json.load(f)
                sessoes = dados.get('sessoes', []) + dados.get('historico', [])
            
            sessoes_mes = [s for s in sessoes if s.get('data', '').startswith(mes_ano)]
            comissoes = calcular_comissoes_por_artista(sessoes_mes)
        else:
            # Mês anterior - buscar no histórico antigo
            comissoes = carregar_historico_antigo(mes_ano, 'comissoes')
        
        return jsonify({
            'success': True,
            'extrato': comissoes
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def carregar_historico_antigo(mes_ano, tipo):
    """Carrega dados históricos de um mês específico"""
    dados_dir = Path(__file__).parent.parent / "dados" / "historico_antigo"
    arquivo = dados_dir / f"{tipo}_{mes_ano}.json"
    
    if arquivo.exists():
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def mover_dados_para_historico():
    """Move dados do mês anterior para o histórico antigo"""
    data_atual = date.today()
    from datetime import timedelta
    mes_anterior = (data_atual.replace(day=1) - timedelta(days=1)).replace(day=1)
    mes_ano_anterior = mes_anterior.strftime("%Y-%m")
    
    dados_dir = Path(__file__).parent.parent / "dados"
    historico_dir = dados_dir / "historico_antigo"
    
    # Criar diretório se não existir
    historico_dir.mkdir(exist_ok=True)
    
    # Mover pagamentos
    try:
        pagamentos = carregar_pagamentos()
        pagamentos_mes_anterior = [p for p in pagamentos if p.get('data', '').startswith(mes_ano_anterior)]
        
        if pagamentos_mes_anterior:
            arquivo_pagamentos = historico_dir / f"pagamentos_{mes_ano_anterior}.json"
            with open(arquivo_pagamentos, 'w', encoding='utf-8') as f:
                json.dump(pagamentos_mes_anterior, f, ensure_ascii=False, indent=2)
            
            # Remover do arquivo atual
            pagamentos_atual = [p for p in pagamentos if not p.get('data', '').startswith(mes_ano_anterior)]
            with open(dados_dir / "pagamentos.json", 'w', encoding='utf-8') as f:
                json.dump(pagamentos_atual, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao mover pagamentos: {e}")
    
    # Mover comissões
    try:
        with open(dados_dir / "sessoes.json", 'r', encoding='utf-8') as f:
            dados_sessoes = json.load(f)
            sessoes = dados_sessoes.get('sessoes', []) + dados_sessoes.get('historico', [])
        
        sessoes_mes_anterior = [s for s in sessoes if s.get('data', '').startswith(mes_ano_anterior)]
        comissoes_mes_anterior = calcular_comissoes_por_artista(sessoes_mes_anterior)
        
        if comissoes_mes_anterior:
            arquivo_comissoes = historico_dir / f"comissoes_{mes_ano_anterior}.json"
            with open(arquivo_comissoes, 'w', encoding='utf-8') as f:
                json.dump(comissoes_mes_anterior, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao mover comissões: {e}")

def calcular_comissoes_por_artista(sessoes):
    """Calcula comissões por artista baseado nas sessões finalizadas"""
    artistas = {}
    
    for sessao in sessoes:
        artista = sessao.get('artista', 'Desconhecido')
        valor = float(sessao.get('valor', 0))
        
        if artista not in artistas:
            artistas[artista] = {
                'artista': artista,
                'total_sessoes': 0,
                'valor_total': 0,
                'comissao': 0
            }
        
        artistas[artista]['total_sessoes'] += 1
        artistas[artista]['valor_total'] += valor
    
    # Calcular comissões (30% para o artista, 70% para o estúdio)
    for artista in artistas.values():
        artista['comissao'] = artista['valor_total'] * 0.30
    
    return list(artistas.values())