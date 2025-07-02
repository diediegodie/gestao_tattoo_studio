from flask import Blueprint, render_template, request, redirect, url_for, flash
from cadastro_interno.artistas import carregar_artistas, adicionar_artista, salvar_artistas

cadastro_bp = Blueprint("cadastro_bp", __name__, url_prefix="/cadastro")


@cadastro_bp.route("/")
def gerenciar_artistas():
    artistas = carregar_artistas()
    return render_template("cadastro_interno/gerenciar_artistas.html", artistas=artistas)


@cadastro_bp.route("/novo", methods=["POST"])
def novo_artista():
    nome = request.form.get("nome", "").strip()
    if not nome:
        flash("O nome do artista é obrigatório.", "erro")
    else:
        sucesso = adicionar_artista(nome)
        if sucesso:
            flash("Artista cadastrado com sucesso!", "sucesso")
        else:
            flash("Esse artista já está cadastrado.", "erro")
    return redirect(url_for("cadastro_bp.gerenciar_artistas"))


@cadastro_bp.route("/editar/<string:nome_antigo>", methods=["GET", "POST"])
def editar_artista(nome_antigo):
    artistas = carregar_artistas()

    if request.method == "POST":
        novo_nome = request.form.get("nome", "").strip()

        if not novo_nome:
            flash("O nome do artista é obrigatório.", "erro")
            return render_template("cadastro_interno/editar_artista.html", nome=nome_antigo)

        if novo_nome in artistas and novo_nome != nome_antigo:
            flash("Esse nome já está cadastrado.", "erro")
            return render_template("cadastro_interno/editar_artista.html", nome=nome_antigo)

        artistas = [novo_nome if a == nome_antigo else a for a in artistas]
        salvar_artistas(artistas)
        flash("Artista atualizado com sucesso!", "sucesso")
        return redirect(url_for("cadastro_bp.gerenciar_artistas"))

    return render_template("cadastro_interno/editar_artista.html", nome=nome_antigo)


@cadastro_bp.route("/excluir/<string:nome>")
def excluir_artista(nome):
    artistas = carregar_artistas()
    artistas = [a for a in artistas if a != nome]
    salvar_artistas(artistas)
    flash("Artista excluído com sucesso.", "sucesso")
    return redirect(url_for("cadastro_bp.gerenciar_artistas"))
