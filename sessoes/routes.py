from flask import Blueprint, render_template, request, redirect, url_for, flash
from sessoes.agendamento import carregar_agendamentos, agendar_sessao, excluir_agendamento

sessoes_bp = Blueprint("sessoes_bp", __name__, url_prefix="/sessoes")

@sessoes_bp.route("/")
def listar_sessoes():
    sessoes = carregar_agendamentos()
    return render_template("sessoes/sessoes.html", sessoes=sessoes)

@sessoes_bp.route("/novo", methods=["GET", "POST"])
def nova_sessao():
    if request.method == "POST":
        cliente = request.form["cliente"]
        artista = request.form["artista"]
        data = request.form["data"]
        hora = request.form["hora"]
        observacoes = request.form.get("observacoes", "")
        agendar_sessao(cliente, artista, data, hora, observacoes)
        flash("Sessão agendada com sucesso!", "sucesso")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    return render_template("sessoes/nova_sessao.html")

@sessoes_bp.route("/excluir/<int:indice>", methods=["GET"])
def excluir_agendamento_route(indice):
    excluir_agendamento(indice)
    flash("Agendamento excluído com sucesso.", "sucesso")
    return redirect(url_for("sessoes_bp.listar_sessoes"))
