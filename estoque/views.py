from flask import Blueprint, render_template, request, redirect, url_for, flash
from estoque.produtos import carregar_produtos, cadastrar_produto, excluir_produto

estoque_bp = Blueprint("estoque_bp", __name__, url_prefix="/estoque")


@estoque_bp.route("/")
def listar_produtos():
    produtos = carregar_produtos()
    return render_template("estoque/estoque.html", produtos=produtos)


@estoque_bp.route("/novo", methods=["GET", "POST"])
def novo_produto():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        valor_unitario_str = request.form.get("valor_unitario", "").strip()
        quantidade_str = request.form.get("quantidade", "").strip()

        erros = []

        if not nome:
            erros.append("Nome é obrigatório.")
        try:
            valor_unitario = float(valor_unitario_str)
            if valor_unitario <= 0:
                erros.append("Valor unitário deve ser maior que zero.")
        except ValueError:
            erros.append("Valor unitário inválido.")

        try:
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                erros.append("Quantidade deve ser maior que zero.")
        except ValueError:
            erros.append("Quantidade inválida.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template(
                "estoque/novo_produto.html",
                nome=nome,
                descricao=descricao,
                valor_unitario=valor_unitario_str,
                quantidade=quantidade_str,
            )

        total = valor_unitario * quantidade
        cadastrar_produto(nome, descricao, valor_unitario, quantidade, total)
        flash("Produto cadastrado com sucesso!", "sucesso")
        return redirect(url_for("estoque_bp.listar_produtos"))

    return render_template("estoque/novo_produto.html")


@estoque_bp.route("/excluir/<nome>")
def excluir_produto_route(nome):
    excluir_produto(nome)
    flash(f"Produto '{nome}' excluído com sucesso!", "sucesso")
    return redirect(url_for("estoque_bp.listar_produtos"))
