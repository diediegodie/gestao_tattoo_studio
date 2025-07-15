from flask import Blueprint, render_template, request, flash, jsonify
from financeiro.caixa import gerar_extrato_mensal
from datetime import datetime

extrato_bp = Blueprint("extrato_bp", __name__, url_prefix="/extrato")

# Meses e anos disponíveis
MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}
ANOS = list(range(2020, datetime.now().year + 2))


@extrato_bp.route("/", methods=["GET", "POST"])
def extrato_mensal():
    dados_extrato = {
        "extrato": [],
        "total": 0,
        "completo": True,
        "comissoes": [],
        "total_comissoes": 0,
        "sessoes_arquivadas": [],
    }
    mes = ano = None

    if request.method == "POST":
        try:
            mes = int(request.form.get("mes", 0))
            ano = int(request.form.get("ano", 0))

            if not (1 <= mes <= 12) or not (2000 <= ano <= 2100):
                flash(
                    "Período inválido. Verifique mês (1-12) e ano (2000-2100).", "erro"
                )
            else:
                resultado = gerar_extrato_mensal(mes, ano)
                if not resultado or not isinstance(resultado, dict):
                    flash("Erro ao gerar extrato.", "erro")
                else:
                    # Guarantee all expected keys exist
                    for k, v in dados_extrato.items():
                        if k not in resultado:
                            resultado[k] = v
                    dados_extrato = resultado
                    if not resultado["completo"]:
                        flash(
                            "Atenção: Mês atual ainda em andamento. Dados parciais.",
                            "aviso",
                        )
                    if (
                        not resultado["extrato"]
                        and not resultado["comissoes"]
                        and not resultado["sessoes_arquivadas"]
                    ):
                        flash(
                            "Nenhum dado encontrado para o período informado.",
                            "info",
                        )
        except ValueError:
            flash("Valores inválidos para mês/ano.", "erro")

    return render_template(
        "financeiro/extrato_mensal.html",
        extrato=dados_extrato["extrato"],
        total=dados_extrato["total"],
        mes=mes,
        ano=ano,
        completo=dados_extrato["completo"],
        comissoes=dados_extrato["comissoes"],
        total_comissoes=dados_extrato["total_comissoes"],
        sessoes_arquivadas=dados_extrato["sessoes_arquivadas"],
        pagamentos_arquivados=dados_extrato.get("pagamentos_arquivados", []),
        meses=MESES,
        anos=ANOS,
        datetime=datetime,
    )


@extrato_bp.route("/dados/<mes_ano>")
def dados_extrato(mes_ano):
    try:
        # Parse do formato YYYY-MM
        ano, mes = mes_ano.split("-")
        mes = int(mes)
        ano = int(ano)

        if not (1 <= mes <= 12) or not (2000 <= ano <= 2100):
            return jsonify({"success": False, "error": "Período inválido"})

        resultado = gerar_extrato_mensal(mes, ano)
        if resultado is None:
            return jsonify({"success": False, "error": "Erro ao gerar extrato"})

        return jsonify(
            {
                "success": True,
                "extrato": resultado["extrato"],
                "total": resultado["total"],
            }
        )

    except (ValueError, AttributeError):
        return jsonify({"success": False, "error": "Formato de data inválido"})
