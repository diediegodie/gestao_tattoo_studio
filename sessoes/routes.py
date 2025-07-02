from flask import Blueprint, render_template, request, redirect, url_for, flash
from sessoes.agendamento import (
    carregar_agendamentos,
    salvar_agendamentos,
    agendar_sessao,
    excluir_agendamento,
)
from datetime import datetime

sessoes_bp = Blueprint("sessoes_bp", __name__, url_prefix="/sessoes")

@sessoes_bp.route("/")
def listar_sessoes():
    sessoes = carregar_agendamentos()
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    if data_inicio and data_fim:
        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
            sessoes = [s for s in sessoes if inicio <= datetime.strptime(s["data"], "%Y-%m-%d").date() <= fim]
        except ValueError:
            flash("Formato de data inválido.", "erro")

    return render_template("sessoes/sessoes.html", sessoes=sessoes)

@sessoes_bp.route("/nova", methods=["GET", "POST"])
def nova_sessao():
    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()
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
                observacoes=observacoes,
            )

        agendar_sessao(cliente, artista, data, hora, observacoes)
        flash("Sessão agendada com sucesso!", "sucesso")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    return render_template("sessoes/nova_sessao.html")

@sessoes_bp.route("/excluir/<int:indice>")
def excluir_agendamento_route(indice):
    excluir_agendamento(indice)
    flash("Agendamento excluído com sucesso!", "sucesso")
    return redirect(url_for("sessoes_bp.listar_sessoes"))

@sessoes_bp.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar_agendamento(indice):
    agendamentos = carregar_agendamentos()

    if indice < 0 or indice >= len(agendamentos):
        flash("Agendamento não encontrado.", "erro")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    sessao = agendamentos[indice]

    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()
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
            return render_template("sessoes/editar_sessao.html", sessao=sessao, indice=indice)

        # Atualiza os dados
        sessao["cliente"] = cliente
        sessao["artista"] = artista
        sessao["data"] = data
        sessao["hora"] = hora
        sessao["observacoes"] = observacoes

        salvar_agendamentos(agendamentos)
        flash("Agendamento atualizado com sucesso!", "sucesso")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    return render_template("sessoes/editar_sessao.html", sessao=sessao, indice=indice)
