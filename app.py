from flask import Flask, render_template, request, redirect, url_for, flash
from financeiro.caixa import carregar_pagamentos, registrar_pagamento
from estoque.produtos import carregar_produtos, cadastrar_produto, excluir_produto
from sessoes.agendamento import carregar_agendamentos, agendar_sessao
from estoque import estoque_bp


app = Flask(__name__)
app.secret_key = "1234"


# --- ROTAS ESTOQUE ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/estoque")
def listar_produtos():
    produtos = carregar_produtos()
    return render_template("estoque.html", produtos=produtos)


@app.route("/estoque/novo", methods=["GET", "POST"])
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
                "novo_produto.html",
                nome=nome,
                descricao=descricao,
                valor_unitario=valor_unitario_str,
                quantidade=quantidade_str,
            )

        total = valor_unitario * quantidade
        cadastrar_produto(nome, descricao, valor_unitario, quantidade, total)
        flash("Produto cadastrado com sucesso!", "sucesso")
        return redirect(url_for("listar_produtos"))

    return render_template("novo_produto.html")

app.register_blueprint(estoque_bp)

# --- ROTAS SESSÕES ---
@app.route("/sessoes")
def listar_sessoes():
    sessoes = carregar_agendamentos()
    return render_template("sessoes.html", sessoes=sessoes)


@app.route("/sessoes/novo", methods=["GET", "POST"])
def nova_sessao():
    if request.method == "POST":
        cliente = request.form["cliente"]
        artista = request.form["artista"]
        data = request.form["data"]
        hora = request.form["hora"]
        observacoes = request.form.get("observacoes", "")

        agendar_sessao(cliente, artista, data, hora, observacoes)
        return redirect(url_for("listar_sessoes"))

    return render_template("nova_sessao.html")


@app.route("/sessoes/excluir/<int:indice>", methods=["GET"])
def excluir_agendamento_route(indice):
    from sessoes.agendamento import excluir_agendamento

    excluir_agendamento(indice)
    flash("Agendamento excluído com sucesso.", "sucesso")
    return redirect(url_for("listar_sessoes"))


# --- ROTAS FINANCEIRO ---
@app.route("/financeiro/registrar", methods=["GET", "POST"])
def registrar_pagamento_route():
    if request.method == "POST":
        valor = request.form.get("valor", "").strip()
        forma = request.form.get("forma_pagamento", "").strip()
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        descricao = request.form.get("descricao", "").strip()

        erros = []
        try:
            valor = float(valor)
            if valor <= 0:
                erros.append("Valor deve ser maior que zero.")
        except ValueError:
            erros.append("Valor inválido.")

        if not forma:
            erros.append("Forma de pagamento é obrigatória.")
        if not cliente:
            erros.append("Cliente é obrigatório.")
        if not artista:
            erros.append("Artista é obrigatório.")
        if not descricao:
            erros.append("Descrição é obrigatória.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template(
                "registrar_pagamento.html",
                valor=valor,
                forma_pagamento=forma,
                cliente=cliente,
                artista=artista,
                descricao=descricao,
            )

        from financeiro.caixa import registrar_pagamento

        registrar_pagamento(valor, forma, cliente, descricao, artista)
        flash("Pagamento registrado com sucesso!", "sucesso")
        return redirect(url_for("listar_pagamentos"))

    return render_template("registrar_pagamento.html")


@app.route("/financeiro")
def listar_pagamentos():
    pagamentos = carregar_pagamentos()
    return render_template("financeiro.html", pagamentos=pagamentos)


@app.route("/financeiro/excluir/<int:indice>", methods=["GET"])
def excluir_pagamento_route(indice):
    from financeiro.caixa import excluir_pagamento

    excluir_pagamento(indice)
    flash("Pagamento excluído com sucesso.", "sucesso")
    return redirect(url_for("listar_pagamentos"))


# --- ROTA EXCLUIR PRODUTO ---
@app.route("/estoque/excluir/<nome>")
def excluir_produto_route(nome):
    excluir_produto(nome)
    flash(f"Produto '{nome}' excluído com sucesso!", "sucesso")
    return redirect(url_for("listar_produtos"))


if __name__ == "__main__":
    app.run(debug=True)
