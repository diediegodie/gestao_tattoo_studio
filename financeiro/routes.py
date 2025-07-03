from flask import Blueprint, render_template, request, redirect, url_for, flash
from financeiro.caixa import (
    carregar_pagamentos,
    registrar_pagamento,
    excluir_pagamento,
    salvar_pagamentos,
)
from datetime import datetime
from cadastro_interno.artistas import carregar_artistas

# Lista de formas de pagamento disponíveis
FORMAS_PAGAMENTO = ['Dinheiro', 'Pix', 'Crédito', 'Débito', 'Outros']

financeiro_bp = Blueprint("financeiro_bp", __name__, url_prefix="/financeiro")

@financeiro_bp.route("/")
def listar_pagamentos():
    pagamentos = carregar_pagamentos()
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    if data_inicio and data_fim:
        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
            pagamentos = [
                p for p in pagamentos
                if inicio <= datetime.strptime(p["data"], "%Y-%m-%d").date() <= fim
            ]
        except ValueError:
            flash("Formato de data inválido.", "erro")

    return render_template("financeiro/financeiro.html", pagamentos=pagamentos)

@financeiro_bp.route("/registrar", methods=["GET", "POST"])
def registrar_pagamento_route():
    artistas = carregar_artistas()

    if request.method == "POST":
        valor = request.form.get("valor", "").strip()
        forma = request.form.get("forma_pagamento", "").strip()
        outra_forma = request.form.get("outra_forma_pagamento", "").strip()
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        descricao = request.form.get("descricao", "").strip()

        erros = []

        # Validação do valor
        if not valor:
            erros.append("Valor é obrigatório.")
        try:
            valor_float = float(valor)
            if valor_float <= 0:
                erros.append("Valor deve ser maior que zero.")
        except ValueError:
            erros.append("Valor inválido. Use ponto como separador decimal.")

        # Validação da forma de pagamento
        if not forma:
            erros.append("Forma de pagamento é obrigatória.")
        elif forma == "Outros" and not outra_forma:
            erros.append("Por favor especifique a forma de pagamento")
        elif forma not in FORMAS_PAGAMENTO:
            erros.append("Forma de pagamento inválida.")

        # Validações dos demais campos
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
                outra_forma_pagamento=outra_forma,
                cliente=cliente,
                artista=artista,
                descricao=descricao,
                artistas=artistas,
                formas_pagamento=FORMAS_PAGAMENTO
            )

        # Usa a forma customizada se for "Outros"
        forma_final = outra_forma if forma == "Outros" else forma

        registrar_pagamento(valor_float, forma_final, cliente, descricao, artista)
        flash("Pagamento registrado com sucesso!", "sucesso")
        return redirect(url_for("financeiro_bp.listar_pagamentos"))

    return render_template(
        "financeiro/registrar_pagamento.html",
        artistas=artistas,
        formas_pagamento=FORMAS_PAGAMENTO
    )

@financeiro_bp.route("/excluir/<int:indice>")
def excluir_pagamento_route(indice):
    excluir_pagamento(indice)
    flash("Pagamento excluído com sucesso.", "sucesso")
    return redirect(url_for("financeiro_bp.listar_pagamentos"))

@financeiro_bp.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar_pagamento(indice):
    pagamentos = carregar_pagamentos()
    artistas = carregar_artistas()

    if indice < 0 or indice >= len(pagamentos):
        flash("Pagamento não encontrado.", "erro")
        return redirect(url_for("financeiro_bp.listar_pagamentos"))

    pagamento = pagamentos[indice]

    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        artista = request.form.get("artista", "").strip()
        valor_str = request.form.get("valor", "").strip()
        forma_pagamento = request.form.get("forma_pagamento", "").strip()
        outra_forma = request.form.get("outra_forma_pagamento", "").strip()
        descricao = request.form.get("descricao", "").strip()

        erros = []
        if not cliente or not artista or not valor_str or not forma_pagamento:
            erros.append("Preencha todos os campos obrigatórios.")

        try:
            valor = float(valor_str)
            if valor <= 0:
                erros.append("O valor deve ser maior que zero.")
        except ValueError:
            erros.append("Valor inválido.")

        # Validação específica para edição
        if forma_pagamento == "Outros" and not outra_forma:
            erros.append("Por favor especifique a forma de pagamento")
        elif forma_pagamento not in FORMAS_PAGAMENTO:
            erros.append("Forma de pagamento inválida")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template(
                "financeiro/editar_pagamento.html",
                pagamento=pagamento,
                indice=indice,
                artistas=artistas,
                formas_pagamento=FORMAS_PAGAMENTO
            )

        # Determina a forma de pagamento final
        forma_final = outra_forma if forma_pagamento == "Outros" else forma_pagamento

        pagamento.update({
            "cliente": cliente,
            "artista": artista,
            "valor": valor,
            "forma_pagamento": forma_final,
            "descricao": descricao
        })
        salvar_pagamentos(pagamentos)
        flash("Pagamento atualizado com sucesso!", "sucesso")
        return redirect(url_for("financeiro_bp.listar_pagamentos"))

    # Prepara os dados para edição
    forma_exibicao = pagamento['forma_pagamento']
    outra_forma = ""
    
    if forma_exibicao not in FORMAS_PAGAMENTO:
        forma_exibicao = "Outros"
        outra_forma = pagamento['forma_pagamento']

    return render_template(
        "financeiro/editar_pagamento.html",
        pagamento=pagamento,
        indice=indice,
        artistas=artistas,
        formas_pagamento=FORMAS_PAGAMENTO,
        forma_pagamento=forma_exibicao,
        outra_forma_pagamento=outra_forma
    )