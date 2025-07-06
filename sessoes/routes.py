from flask import Blueprint, render_template, request, redirect, url_for, flash
from sessoes.agendamento import (
    carregar_agendamentos,
    salvar_agendamentos,
    agendar_sessao,
    excluir_agendamento,
    carregar_sessoes_limbo,
    enviar_para_limbo,
    retornar_do_limbo,
    excluir_do_limbo,
)
from datetime import datetime
from cadastro_interno.artistas import carregar_artistas
from sessoes.historico import mover_para_historico
import json

sessoes_bp = Blueprint("sessoes_bp", __name__, url_prefix="/sessoes")

@sessoes_bp.route("/")
def listar_sessoes():
    sessoes = carregar_agendamentos()
    termo = request.args.get("busca", "").strip().lower()
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")
    
    if termo:
        sessoes = [s for s in sessoes if termo in s.get('cliente', '').lower()]

    if data_inicio and data_fim:
        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
            sessoes = [
                s
                for s in sessoes
                if inicio <= datetime.strptime(s["data"], "%Y-%m-%d").date() <= fim
            ]
        except ValueError:
            flash("Formato de data inválido.", "erro")
    
    # Filtrar sessões normais (não no limbo)
    sessoes_normais = [s for s in sessoes if not s.get('no_limbo', False)]
    
    # Carregar sessões do limbo
    sessoes_limbo = carregar_sessoes_limbo()
    
    return render_template("sessoes/sessoes.html", sessoes=sessoes_normais, sessoes_limbo=sessoes_limbo)

@sessoes_bp.route("/fechar/<int:id>", methods=["POST"])
def fechar_sessao(id):
    agendamentos = carregar_agendamentos()
    sessao = next((s for s in agendamentos if s["id"] == id), None)
    
    if sessao:
        # Armazena os dados da sessão na sessão Flask para uso no formulário de pagamento
        from flask import session
        session['sessao_para_pagamento'] = {
            'id': sessao['id'],
            'cliente': sessao['cliente'],
            'artista': sessao['artista'],
            'valor': sessao.get('valor', 0.0),
            'data': sessao['data'],
            'observacoes': sessao.get('observacoes', '')
        }
        
        flash("Sessão pronta para pagamento!", "sucesso")
        return redirect(url_for('financeiro_bp.registrar_pagamento_route'))
    else:
        flash("Sessão não encontrada.", "erro")
        return redirect(url_for('sessoes_bp.listar_sessoes'))

@sessoes_bp.route("/nova", methods=["GET", "POST"])
def nova_sessao():
    artistas = carregar_artistas()

    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()
        valor = request.form.get("valor", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        erros = []

        if not cliente:
            erros.append("Nome do cliente é obrigatório.")
        if not artista:
            erros.append("Nome do artista é obrigatório.")
        if not data:
            erros.append("Data é obrigatória.")
        if not hora:
            erros.append("Hora é obrigatória.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template(
                "sessoes/nova_sessao.html",
                cliente=cliente,
                artista=artista,
                data=data,
                hora=hora,
                valor=valor,
                observacoes=observacoes,
                artistas=artistas,
            )

        agendar_sessao(cliente, artista, data, hora, valor, observacoes)
        flash("Sessão agendada com sucesso!", "sucesso")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    return render_template("sessoes/nova_sessao.html", artistas=artistas)

@sessoes_bp.route("/excluir/<int:indice>")
def excluir_agendamento_route(indice):
    excluir_agendamento(indice)
    flash("Agendamento excluído com sucesso!", "sucesso")
    return redirect(url_for("sessoes_bp.listar_sessoes"))

@sessoes_bp.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar_agendamento(indice):
    agendamentos = carregar_agendamentos()
    artistas = carregar_artistas()

    if indice < 0 or indice >= len(agendamentos):
        flash("Agendamento não encontrado.", "erro")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    sessao = agendamentos[indice]

    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()
        # --- CORREÇÃO 1: Ler o valor do formulário ---
        valor = request.form.get("valor", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        erros = []

        if not cliente:
            erros.append("Nome do cliente é obrigatório.")
        if not artista:
            erros.append("Nome do artista é obrigatório.")
        if not data:
            erros.append("Data é obrigatória.")
        if not hora:
            erros.append("Hora é obrigatória.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template(
                "sessoes/editar_sessao.html",
                sessao=sessao,
                indice=indice,
                artistas=artistas,
            )

        sessao["cliente"] = cliente
        sessao["artista"] = artista
        sessao["data"] = data
        sessao["hora"] = hora
        # --- CORREÇÃO 2: Atualizar o valor na sessão ---
        # Converte para float, ou define como 0.0 se estiver vazio
        sessao["valor"] = float(valor) if valor else 0.0
        sessao["observacoes"] = observacoes

        salvar_agendamentos(agendamentos)
        flash("Agendamento atualizado com sucesso!", "sucesso")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    return render_template(
        "sessoes/editar_sessao.html", sessao=sessao, indice=indice, artistas=artistas
    )

@sessoes_bp.route("/enviar-para-limbo/<int:id>", methods=["POST"])
def enviar_para_limbo_route(id):
    if enviar_para_limbo(id):
        flash("Sessão enviada para o limbo!", "sucesso")
    else:
        flash("Sessão não encontrada.", "erro")
    return redirect(url_for("sessoes_bp.listar_sessoes"))

@sessoes_bp.route("/retornar-do-limbo/<int:id>", methods=["POST"])
def retornar_do_limbo_route(id):
    if retornar_do_limbo(id):
        flash("Sessão retornada dos agendamentos!", "sucesso")
    else:
        flash("Sessão não encontrada no limbo.", "erro")
    return redirect(url_for("sessoes_bp.listar_sessoes"))

@sessoes_bp.route("/excluir-do-limbo/<int:id>", methods=["POST"])
def excluir_do_limbo_route(id):
    if excluir_do_limbo(id):
        flash("Sessão removida definitivamente do limbo!", "sucesso")
    else:
        flash("Sessão não encontrada no limbo.", "erro")
    return redirect(url_for("sessoes_bp.listar_sessoes"))


@sessoes_bp.route("/historico")
def listar_historico():
    try:
        with open("dados/sessoes.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            historico = dados.get("historico", [])
            
            # Processa os dados para garantir que o valor está presente
            sessoes_historico = []
            for sessao in historico:
                # Garante que o valor seja numérico e não seja None
                valor = sessao.get("valor")
                if valor is None or valor == "":
                    valor = 0.0
                else:
                    try:
                        valor = float(valor)
                    except (ValueError, TypeError):
                        valor = 0.0
                
                sessoes_historico.append({
                    "id": sessao.get("id", 0),
                    "data": sessao.get("data", ""),
                    "cliente": sessao.get("cliente", ""),
                    "artista": sessao.get("artista", ""),
                    "valor": valor,
                    "observacoes": sessao.get("observacoes", ""),
                    "data_fechamento": sessao.get("data_fechamento", "")
                })
            
            # Inverter a ordem para mostrar os mais recentes no topo
            sessoes_historico.reverse()
            
            print(f"Dados do histórico processados: {sessoes_historico}")
            
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar histórico: {e}")
        sessoes_historico = []
    
    return render_template("historico/sessoes.html", sessoes=sessoes_historico)




@sessoes_bp.route("/historico/excluir/<int:id>", methods=["POST"])
def excluir_historico(id):
    try:
        with open("dados/sessoes.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {"sessoes_ativas": [], "historico": []}
    
    # Corrige a comparação para garantir que ambos são inteiros e o campo id existe
    dados["historico"] = [
        s for s in dados["historico"]
        if int(s.get("id", -1)) != int(id)
    ]
    
    # Salva as alterações
    with open("dados/sessoes.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    
    flash("Sessão removida do histórico com sucesso!", "sucesso")
    return redirect(url_for('sessoes_bp.listar_historico'))


@sessoes_bp.route("/historico/editar/<int:id>", methods=["GET", "POST"])
def editar_historico(id):
    try:
        with open("dados/sessoes.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {"sessoes_ativas": [], "historico": []}
    
    sessao = next((s for s in dados["historico"] if s.get("id") == id), None)
    
    if not sessao:
        flash("Sessão não encontrada no histórico.", "erro")
        return redirect(url_for('sessoes_bp.listar_historico'))
    
    if request.method == "POST":
        sessao["valor"] = float(request.form.get("valor", 0))
        sessao["observacoes"] = request.form.get("observacoes", "")
        
        with open("dados/sessoes.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        
        flash("Sessão atualizada no histórico!", "sucesso")
        return redirect(url_for('sessoes_bp.listar_historico'))
    
    return render_template("historico/editar.html", sessao=sessao)
