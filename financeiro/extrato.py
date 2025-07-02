from flask import Blueprint, render_template, request, flash
from financeiro.caixa import gerar_extrato_mensal
from datetime import datetime

extrato_bp = Blueprint("extrato_bp", __name__, url_prefix="/extrato")

@extrato_bp.route("/", methods=["GET", "POST"])
def extrato_mensal():
    extrato = []
    mes = ano = None
    if request.method == "POST":
        mes = int(request.form.get("mes", 0))
        ano = int(request.form.get("ano", 0))

        resultado = gerar_extrato_mensal(mes, ano)
        if resultado is None:
            flash("Fechamento não disponível para o mês atual.", "erro")
        elif not resultado:
            flash("Nenhum pagamento encontrado para o período informado.", "erro")
        else:
            extrato = resultado

    return render_template("financeiro/extrato_mensal.html", extrato=extrato, mes=mes, ano=ano)
