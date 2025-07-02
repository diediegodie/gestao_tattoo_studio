from flask import Blueprint, render_template, request, redirect, url_for, flash
from financeiro.caixa import carregar_pagamentos, registrar_pagamento, excluir_pagamento

financeiro_bp = Blueprint("financeiro_bp", __name__, url_prefix="/financeiro")

@financeiro_bp.route("/")
def listar_pagamentos():
    pagamentos = carregar_pagamentos()
    return render_template("financeiro/financeiro.html", pagamentos=pagamentos)

@financeiro_bp.route("/registrar", methods=["GET", "POST"])
def registrar_pagamento_route():
    if request.method == "POST":
        valor = request.form.get("valor", "").strip()
        forma = request.form.get("forma_pagamento", "").strip()
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        descricao = request.form.get("descricao", "").strip()

        erros = []
        try:
            valor_float = float(valor)
            if valor_float <= 0:
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
                "financeiro/registrar_pagamento.html",
                valor=valor,
                forma_pagamento=forma,
                cliente=cliente,
                artista=artista,
                descricao=descricao,
            )

        registrar_pagamento(valor_float, forma, cliente, descricao, artista)
        flash("Pagamento registrado com sucesso!", "sucesso")
        return redirect(url_for("financeiro_bp.listar_pagamentos"))

    return render_template("financeiro/registrar_pagamento.html")

@financeiro_bp.route("/excluir/<int:indice>", methods=["GET"])
def excluir_pagamento_route(indice):
    excluir_pagamento(indice)
    flash("Pagamento excluído com sucesso.", "sucesso")
    return redirect(url_for("financeiro_bp.listar_pagamentos"))
