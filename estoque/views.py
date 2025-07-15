from flask import Blueprint, render_template, request, redirect, url_for, flash
from estoque.produtos import (
    carregar_produtos,
    cadastrar_produto,
    excluir_produto,
    salvar_produtos,
)

estoque_bp = Blueprint("estoque_bp", __name__, url_prefix="/estoque")


@estoque_bp.route("/")
def listar_produtos():
    produtos = carregar_produtos()
    termo = request.args.get("busca", "").strip().lower()

    if termo:
        produtos = [p for p in produtos if termo in p.get("nome", "").lower()]

    return render_template("estoque/estoque.html", produtos=produtos, termo=termo)


@estoque_bp.route("/novo", methods=["GET", "POST"])
def novo_produto():
    if request.method == "POST":
        print("POST recebido")
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        quantidade_str = request.form.get("quantidade", "").strip()

        erros = []

        # Validação dos campos
        if not nome:
            erros.append("Nome do produto é obrigatório.")
        if not quantidade_str:
            erros.append("Quantidade é obrigatória.")
        try:
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                erros.append("Quantidade deve ser maior que zero.")
        except ValueError:
            erros.append("Quantidade inválida. Use apenas números inteiros.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template(
                "estoque/novo_produto.html",
                nome=nome,
                descricao=descricao,
                quantidade=quantidade_str,
            )

        # VERIFICA DUPLICAÇÃO
        produtos = carregar_produtos()
        if any(p["nome"].lower() == nome.lower() for p in produtos):
            flash("Já existe um produto com esse nome.", "erro")
            return render_template(
                "estoque/novo_produto.html",
                nome=nome,
                descricao=descricao,
                quantidade=quantidade_str,
            )

        cadastrar_produto(nome, descricao, quantidade)
        flash("Produto cadastrado com sucesso!", "sucesso")
        return redirect(url_for("estoque_bp.listar_produtos"))

    return render_template("estoque/novo_produto.html")


@estoque_bp.route("/excluir/<nome>", methods=["POST", "GET"])
def excluir_produto_route(nome):
    excluir_produto(nome)
    flash(f"Produto '{nome}' excluído com sucesso!", "sucesso")
    return redirect(url_for("estoque_bp.listar_produtos"))


@estoque_bp.route("/editar/<nome>", methods=["GET", "POST"])
def editar_produto(nome):
    produtos = carregar_produtos()
    produto = next((p for p in produtos if p["nome"] == nome), None)

    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("estoque_bp.listar_produtos"))

    if request.method == "POST":
        novo_nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        quantidade_str = request.form.get("quantidade", "").strip()

        erros = []

        if not novo_nome:
            erros.append("Nome é obrigatório.")

        try:
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                erros.append("Quantidade deve ser maior que zero.")
        except ValueError:
            erros.append("Quantidade inválida.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template("estoque/editar_produto.html", produto=produto)

        # Verifica se já existe outro produto com o mesmo nome
        if novo_nome.lower() != nome.lower() and any(
            p["nome"].lower() == novo_nome.lower() for p in produtos
        ):
            flash("Já existe outro produto com esse nome.", "erro")
            return render_template("estoque/editar_produto.html", produto=produto)

        # Atualiza produto
        produto["nome"] = novo_nome
        produto["descricao"] = descricao
        produto["quantidade"] = quantidade

        salvar_produtos(produtos)
        flash("Produto atualizado com sucesso!", "sucesso")
        return redirect(url_for("estoque_bp.listar_produtos"))

    return render_template("estoque/editar_produto.html", produto=produto)
