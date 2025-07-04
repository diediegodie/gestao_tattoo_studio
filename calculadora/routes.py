from flask import render_template, request, url_for
from calculadora import calculadora_bp

@calculadora_bp.route("/")
def calculadora():
    sessao_id = request.args.get('sessao_id')
    return render_template("calculadora/calculadora.html", sessao_id=sessao_id)

@calculadora_bp.route("/calcular", methods=["POST"])
def calcular():
    valor = float(request.form.get('valor'))
    porcentagem = float(request.form.get('porcentagem'))
    sessao_id = request.form.get('sessao_id')
    
    comissao = valor * (porcentagem / 100)
    estudio = valor - comissao
    
    return render_template("calculadora/resultado.html",
                         valor=valor,
                         porcentagem=porcentagem,
                         comissao=comissao,
                         estudio=estudio,
                         sessao_id=sessao_id)

@calculadora_bp.route("/confirmar", methods=["POST"])
def confirmar():
    if request.form.get('sessao_id'):
        mover_para_historico(
            sessao_id=int(request.form.get('sessao_id')),
            valor_pago=float(request.form.get('valor')),
            porcentagem=float(request.form.get('porcentagem'))
        )
    return redirect(url_for('historico_bp.historico_sessoes'))