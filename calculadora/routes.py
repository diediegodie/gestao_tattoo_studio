from flask import render_template, request, url_for, redirect, flash
from calculadora import calculadora_bp
from sessoes.historico import mover_para_historico

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
    sessao_id_str = request.form.get('sessao_id')
    valor_pago_str = request.form.get('valor')
    porcentagem_str = request.form.get('porcentagem')

    if not sessao_id_str or not valor_pago_str or not porcentagem_str:
        flash("ID da sessão, valor ou porcentagem não fornecido.", "erro")
        return redirect(url_for('sessoes_bp.listar_sessoes'))

    sessao_id = int(sessao_id_str)
    valor_pago = float(valor_pago_str)
    porcentagem = float(porcentagem_str)
    comissao = round(valor_pago * (porcentagem / 100), 2)

    if mover_para_historico(sessao_id=sessao_id, valor_final=valor_pago, comissao=comissao):
        flash(f"Sessão movida para o histórico com sucesso! Comissão: R$ {comissao:.2f} ({porcentagem:.1f}%)", "sucesso")
    else:
        flash("ERRO: Sessão não encontrada ou falha ao mover para o histórico.", "erro")
    
    return redirect(url_for('sessoes_bp.listar_sessoes'))