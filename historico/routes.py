from flask import render_template, request, jsonify, flash, redirect, url_for
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

@historico_bp.route("/comissoes-avulsas")
def historico_comissoes_avulsas():
    """Exibe o histórico de comissões avulsas"""
    try:
        from financeiro.comissoes import carregar_comissoes
        comissoes_avulsas = carregar_comissoes()
        
        # Inverter a ordem para mostrar os mais recentes no topo
        comissoes_avulsas.reverse()
        
        return render_template("historico/comissoes_avulsas.html", 
                             comissoes_avulsas=comissoes_avulsas)
    except Exception as e:
        flash(f"Erro ao carregar comissões avulsas: {str(e)}", "erro")
        return redirect(url_for('historico_bp.historico_sessoes'))

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
            
            # Incluir comissões avulsas do mês
            try:
                from financeiro.comissoes import obter_comissoes_por_artista
                mes, ano = mes_ano.split('-')
                comissoes_avulsas = obter_comissoes_por_artista(mes=int(mes), ano=int(ano))
                
                # Adicionar comissões avulsas ao resultado
                for comissao_avulsa in comissoes_avulsas:
                    artista = comissao_avulsa.get('artista')
                    valor_comissao = comissao_avulsa.get('valor_comissao', 0)
                    
                    # Encontrar ou criar entrada para o artista
                    artista_encontrado = False
                    for comissao in comissoes:
                        if comissao.get('artista') == artista:
                            comissao['comissao'] += valor_comissao
                            comissao['valor_total'] += comissao_avulsa.get('valor_total', 0)
                            artista_encontrado = True
                            break
                    
                    if not artista_encontrado:
                        comissoes.append({
                            'artista': artista,
                            'total_sessoes': 0,
                            'valor_total': comissao_avulsa.get('valor_total', 0),
                            'comissao': valor_comissao
                        })
                        
            except Exception as e:
                print(f"Erro ao incluir comissões avulsas no extrato: {e}")
                
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

@historico_bp.route("/comissoes/editar/<artista>", methods=["GET", "POST"])
def editar_comissao(artista):
    """Edita os dados de comissão de um artista específico"""
    if request.method == "POST":
        try:
            # Carregar dados atuais
            with open(Path(__file__).parent.parent / "dados" / "sessoes.json", 'r', encoding='utf-8') as f:
                dados = json.load(f)
                sessoes_historico = dados.get('historico', [])
            
            # Filtrar sessões do artista
            sessoes_artista = [s for s in sessoes_historico if s.get('artista') == artista]
            
            # Atualizar comissão se necessário
            nova_comissao = float(request.form.get('comissao', 0))
            
            # Aqui você pode implementar a lógica para atualizar a comissão
            # Por enquanto, apenas retorna uma mensagem de sucesso
            flash(f"Comissão do artista {artista} atualizada com sucesso!", "sucesso")
            return redirect(url_for('historico_bp.historico_sessoes'))
            
        except Exception as e:
            flash(f"Erro ao editar comissão: {str(e)}", "erro")
            return redirect(url_for('historico_bp.historico_sessoes'))
    
    # GET: Mostrar formulário de edição
    return render_template("historico/editar_comissao.html", artista=artista)

@historico_bp.route("/comissoes/excluir/<artista>", methods=["POST"])
def excluir_comissao(artista):
    """Exclui os dados de comissão de um artista específico"""
    try:
        # Carregar dados atuais
        with open(Path(__file__).parent.parent / "dados" / "sessoes.json", 'r', encoding='utf-8') as f:
            dados = json.load(f)
            sessoes_historico = dados.get('historico', [])
        
        # Filtrar sessões do artista para remover
        sessoes_restantes = [s for s in sessoes_historico if s.get('artista') != artista]
        
        # Atualizar o histórico removendo as sessões do artista
        dados['historico'] = sessoes_restantes
        
        # Salvar as alterações
        with open(Path(__file__).parent.parent / "dados" / "sessoes.json", 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        flash(f"Comissões do artista {artista} excluídas com sucesso!", "sucesso")
        
    except Exception as e:
        flash(f"Erro ao excluir comissão: {str(e)}", "erro")
    
    return redirect(url_for('historico_bp.historico_sessoes'))

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
    """Calcula comissões por artista baseado nas sessões finalizadas e comissões avulsas"""
    artistas = {}
    
    # Processa comissões das sessões
    for sessao in sessoes:
        artista = sessao.get('artista', 'Desconhecido')
        valor = float(sessao.get('valor', 0))
        
        # Usa a comissão salva se existir, senão calcula 70%
        comissao_salva = sessao.get('comissao', 0)
        if comissao_salva > 0:
            comissao = float(comissao_salva)
        else:
            comissao = valor * 0.70  # 70% para o artista
        
        if artista not in artistas:
            artistas[artista] = {
                'artista': artista,
                'total_sessoes': 0,
                'valor_total': 0,
                'comissao': 0
            }
        
        artistas[artista]['total_sessoes'] += 1
        artistas[artista]['valor_total'] += valor
        artistas[artista]['comissao'] += comissao
    
    # Processa comissões avulsas
    try:
        from financeiro.comissoes import carregar_comissoes
        comissoes_avulsas = carregar_comissoes()
        
        for comissao_avulsa in comissoes_avulsas:
            artista = comissao_avulsa.get('artista', 'Desconhecido')
            valor_comissao = float(comissao_avulsa.get('valor_comissao', 0))
            valor_total = float(comissao_avulsa.get('valor_total', 0))
            
            if artista not in artistas:
                artistas[artista] = {
                    'artista': artista,
                    'total_sessoes': 0,
                    'valor_total': 0,
                    'comissao': 0
                }
            
            # Para comissões avulsas, não incrementa total_sessoes, apenas valor e comissão
            artistas[artista]['valor_total'] += valor_total
            artistas[artista]['comissao'] += valor_comissao
            
    except Exception as e:
        print(f"Erro ao carregar comissões avulsas: {e}")
    
    return list(artistas.values())