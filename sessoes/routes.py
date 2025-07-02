from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sessoes.agendamento import (
    carregar_agendamentos,
    agendar_sessao,
    excluir_agendamento,
)

sessoes_bp = Blueprint("sessoes_bp", __name__, url_prefix="/sessoes")


@sessoes_bp.route("/")
def listar_sessoes():
    sessoes = carregar_agendamentos()
    return render_template("sessoes/sessoes.html", sessoes=sessoes)


@sessoes_bp.route("/novo", methods=["GET", "POST"])
def nova_sessao():
    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        erros = []

        # Valida campos obrigatórios
        if not cliente:
            erros.append("Cliente é obrigatório.")
        if not artista:
            erros.append("Artista é obrigatório.")
        if not data:
            erros.append("Data é obrigatória.")
        if not hora:
            erros.append("Hora é obrigatória.")

        # Valida formato da data e hora
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            erros.append("Formato de data inválido. Use AAAA-MM-DD.")

        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            erros.append("Formato de hora inválido. Use HH:MM.")

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


@sessoes_bp.route("/excluir/<int:indice>", methods=["GET"])
def excluir_agendamento_route(indice):
    excluir_agendamento(indice)
    flash("Agendamento excluído com sucesso.", "sucesso")
    return redirect(url_for("sessoes_bp.listar_sessoes"))


@sessoes_bp.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar_agendamento(indice):
    sessoes = carregar_sessoes()
    if indice < 0 or indice >= len(sessoes):
        flash("Agendamento não encontrado.", "erro")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    sessao = sessoes[indice]

    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        erros = []
        if not cliente or not artista or not data or not hora:
            erros.append("Todos os campos obrigatórios devem ser preenchidos.")

        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            erros.append("Data inválida. Use o formato YYYY-MM-DD.")

        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            erros.append("Hora inválida. Use o formato HH:MM.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template(
                "sessoes/editar_sessao.html", sessao=sessao, indice=indice
            )

        # Atualiza os dados
        sessao.update(
            {
                "cliente": cliente,
                "artista": artista,
                "data": data,
                "hora": hora,
                "observacoes": observacoes,
            }
        )
        salvar_sessoes(sessoes)
        flash("Sessão atualizada com sucesso!", "sucesso")
        return redirect(url_for("sessoes_bp.listar_sessoes"))

    return render_template("sessoes/editar_sessao.html", sessao=sessao, indice=indice)
