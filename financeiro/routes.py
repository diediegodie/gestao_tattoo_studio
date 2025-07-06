from flask import Blueprint, render_template, request, redirect, url_for, flash
from financeiro.caixa import (
    carregar_pagamentos,
    registrar_pagamento,
    excluir_pagamento,
    salvar_pagamentos,
    CAMINHO_PAGAMENTOS,
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

    # Inverter a ordem para mostrar os mais recentes no topo
    pagamentos.reverse()

    return render_template("financeiro/financeiro.html", 
                         pagamentos=pagamentos,
                         formas_pagamento=FORMAS_PAGAMENTO)

@financeiro_bp.route("/registrar", methods=["GET", "POST"])
def registrar_pagamento_route():
    artistas = carregar_artistas()
    
    if request.method == "POST":
        try:
            novo_pagamento = {
                "data": request.form.get("data"),
                "cliente": request.form.get("cliente"),
                "artista": request.form.get("artista"),
                "valor": float(request.form.get("valor", 0)),
                "forma_pagamento": request.form.get("forma_pagamento"),
                "descricao": request.form.get("descricao", "")
            }
            
            if registrar_pagamento(novo_pagamento):
                # Verifica se há uma sessão pendente para finalizar
                from flask import session
                sessao_pendente = session.get('sessao_para_pagamento')
                
                if sessao_pendente:
                    # Move a sessão para o histórico
                    from sessoes.historico import mover_para_historico
                    from sessoes.agendamento import carregar_agendamentos, salvar_agendamentos
                    
                    if mover_para_historico(sessao_id=sessao_pendente['id'], valor_final=novo_pagamento['valor']):
                        # Remove da lista de agendamentos ativos
                        agendamentos = carregar_agendamentos()
                        agendamentos = [s for s in agendamentos if s["id"] != sessao_pendente['id']]
                        salvar_agendamentos(agendamentos)
                        
                        # Limpa a sessão pendente
                        session.pop('sessao_para_pagamento', None)
                        
                        flash("Pagamento registrado e sessão finalizada com sucesso!", "sucesso")
                        return redirect(url_for("historico_bp.historico_sessoes"))
                    else:
                        flash("Pagamento registrado, mas erro ao finalizar sessão.", "erro")
                else:
                    flash("Pagamento registrado com sucesso!", "sucesso")
                
                return redirect(url_for("financeiro_bp.listar_pagamentos"))
            else:
                flash("Erro ao registrar pagamento.", "erro")
        except Exception as e:
            print(f"Erro no registro: {e}")
            flash("Dados inválidos no formulário.", "erro")
    
    # Pré-preenche os dados se há uma sessão pendente
    from flask import session
    sessao_pendente = session.get('sessao_para_pagamento', {})
    
    return render_template("financeiro/registrar_pagamento.html",
                         artistas=artistas,
                         formas_pagamento=FORMAS_PAGAMENTO,
                         sessao_pendente=sessao_pendente)

@financeiro_bp.route("/excluir/<int:indice>")
def excluir_pagamento_route(indice):
    if excluir_pagamento(indice):
        flash("Pagamento excluído com sucesso.", "sucesso")
    else:
        flash("Erro ao excluir pagamento.", "erro")
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
        try:
            # Determina a forma de pagamento final
            forma_pagamento = request.form.get("forma_pagamento")
            outra_forma = request.form.get("outra_forma_pagamento", "").strip()
            
            forma_final = outra_forma if forma_pagamento == "Outros" else forma_pagamento

            pagamento.update({
                "data": request.form.get("data"),
                "cliente": request.form.get("cliente"),
                "artista": request.form.get("artista"),
                "valor": float(request.form.get("valor", 0)),
                "forma_pagamento": forma_final,
                "descricao": request.form.get("descricao", "")
            })
            
            if salvar_pagamentos(pagamentos):
                flash("Pagamento atualizado com sucesso!", "sucesso")
                return redirect(url_for("financeiro_bp.listar_pagamentos"))
            else:
                flash("Erro ao atualizar pagamento.", "erro")
        except Exception as e:
            print(f"Erro na edição: {e}")
            flash("Dados inválidos no formulário.", "erro")

    # Prepara os dados para exibição
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
