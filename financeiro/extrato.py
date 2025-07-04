from flask import Blueprint, render_template, request, flash
from financeiro.caixa import gerar_extrato_mensal
from datetime import datetime  # Adicione esta importação

extrato_bp = Blueprint("extrato_bp", __name__, url_prefix="/extrato")

@extrato_bp.route("/", methods=["GET", "POST"])
def extrato_mensal():
    dados_extrato = {"extrato": [], "total": 0, "completo": True}
    mes = ano = None
    
    if request.method == "POST":
        try:
            mes = int(request.form.get("mes", 0))
            ano = int(request.form.get("ano", 0))
            
            if not (1 <= mes <= 12) or not (2000 <= ano <= 2100):
                flash("Período inválido. Verifique mês (1-12) e ano (2000-2100).", "erro")
            else:
                resultado = gerar_extrato_mensal(mes, ano)
                if resultado is None:
                    flash("Erro ao gerar extrato.", "erro")
                else:
                    dados_extrato = resultado
                    if not resultado["completo"]:
                        flash("Atenção: Mês atual ainda em andamento. Dados parciais.", "aviso")
                    if not resultado["extrato"]:
                        flash("Nenhum pagamento encontrado para o período informado.", "info")
        except ValueError:
            flash("Valores inválidos para mês/ano.", "erro")
    
    return render_template(
        "financeiro/extrato_mensal.html",
        extrato=dados_extrato["extrato"],
        total=dados_extrato["total"],
        mes=mes,
        ano=ano,
        completo=dados_extrato["completo"],
        datetime=datetime  # Adicione esta linha para passar o datetime para o template
    )