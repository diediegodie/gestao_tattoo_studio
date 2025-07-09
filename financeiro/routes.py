from flask import Blueprint, render_template, request, redirect, url_for, flash
from financeiro.caixa import (
    carregar_pagamentos,
    registrar_pagamento,
    excluir_pagamento,
    salvar_pagamentos,
    CAMINHO_PAGAMENTOS,
)
from financeiro.comissoes import registrar_comissao_avulsa
from datetime import datetime
from cadastro_interno.artistas import carregar_artistas
from sessoes.historico import mover_para_historico

# Lista de formas de pagamento disponíveis
FORMAS_PAGAMENTO = ["Dinheiro", "Pix", "Crédito", "Débito", "Outros"]

financeiro_bp = Blueprint("financeiro_bp", __name__, url_prefix="/financeiro")


@financeiro_bp.route("/")
def listar_pagamentos():
    # Carrega pagamentos do historico_pagamentos.json
    from pathlib import Path
    import json

    caminho = Path(__file__).parent.parent / "dados" / "historico_pagamentos.json"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception:
        pagamentos = []

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    if data_inicio and data_fim:
        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
            pagamentos = [
                p
                for p in pagamentos
                if inicio <= datetime.strptime(p["data"], "%Y-%m-%d").date() <= fim
            ]
        except ValueError:
            flash("Formato de data inválido.", "erro")

    # Inverter a ordem para mostrar os mais recentes no topo
    pagamentos.reverse()

    return render_template(
        "financeiro/financeiro.html",
        pagamentos=pagamentos,
        formas_pagamento=FORMAS_PAGAMENTO,
    )


@financeiro_bp.route("/registrar", methods=["GET", "POST"])
def registrar_pagamento_route():
    from financeiro.caixa import carregar_pagamentos, salvar_pagamentos
    from financeiro.comissoes import (
        carregar_comissoes,
        salvar_comissoes,
        gerar_id_comissao,
    )
    from pathlib import Path
    import json
    from datetime import datetime

    def carregar_historico_pagamentos():
        caminho = Path(__file__).parent.parent / "dados" / "historico_pagamentos.json"
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def salvar_historico_pagamentos(lista):
        caminho = Path(__file__).parent.parent / "dados" / "historico_pagamentos.json"
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(lista, f, indent=4, ensure_ascii=False)
        except Exception as e:
            flash("Erro ao salvar histórico de pagamentos.", "erro")

    def carregar_historico_comissoes():
        caminho = Path(__file__).parent.parent / "dados" / "historico_comissoes.json"
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def salvar_historico_comissoes(lista):
        caminho = Path(__file__).parent.parent / "dados" / "historico_comissoes.json"
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(lista, f, indent=4, ensure_ascii=False)
        except Exception as e:
            flash("Erro ao salvar histórico de comissões.", "erro")

    artistas = carregar_artistas()
    if request.method == "POST":
        try:
            valor_str = request.form.get("valor", "0").replace(",", ".")
            valor = float(valor_str) if valor_str else 0.0
            artista = request.form.get("artista", "").strip()
            porcentagem_str = request.form.get("porcentagem_comissao", "0").replace(
                ",", "."
            )
            porcentagem = float(porcentagem_str) if porcentagem_str else 0.0
            descricao = request.form.get("descricao", "").strip()
            data = request.form.get("data") or datetime.now().strftime("%Y-%m-%d")
            cliente = request.form.get("cliente", "").strip()
            forma_pagamento = request.form.get("forma_pagamento", "").strip()
            sessao_id = request.form.get("sessao_id") or request.args.get("sessao_id")

            # Monta o pagamento
            novo_pagamento = {
                "data": data,
                "cliente": cliente,
                "artista": artista,
                "valor": valor,
                "forma_pagamento": forma_pagamento,
                "descricao": descricao,
                "porcentagem_comissao": porcentagem,
            }

            # Salva no histórico de pagamentos (arquivo separado)
            historico_pagamentos = carregar_historico_pagamentos()
            historico_pagamentos.append(novo_pagamento)
            salvar_historico_pagamentos(historico_pagamentos)

            # Se artista preenchido e porcentagem > 0, salva comissão
            if artista and porcentagem > 0:
                valor_comissao = round(valor * (porcentagem / 100), 2)
                if valor_comissao > 0:
                    comissoes = carregar_comissoes()
                    nova_comissao = {
                        "id": gerar_id_comissao(comissoes),
                        "artista": artista,
                        "valor_comissao": valor_comissao,
                        "valor_total": valor,
                        "cliente": cliente,
                        "data": data,
                        "data_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "descricao": descricao,
                        "tipo": "pagamento_avulso",
                    }
                    # Sempre salva comissão avulsa, independente de ser pagamento de sessão ou não
                    comissoes.append(nova_comissao)
                    salvar_comissoes(comissoes)
                    # Salva também no histórico de comissões
                    historico_comissoes = carregar_historico_comissoes()
                    historico_comissoes.append(nova_comissao)
                    salvar_historico_comissoes(historico_comissoes)
                    flash(
                        f"Pagamento e comissão registrados com sucesso! Comissão: R$ {valor_comissao:.2f} ({porcentagem:.1f}%)",
                        "sucesso",
                    )
                else:
                    flash(
                        "Pagamento registrado, mas comissão não foi salva pois o valor calculado foi zero.",
                        "aviso",
                    )
            else:
                flash("Pagamento registrado com sucesso!", "sucesso")

            # Se for pagamento de sessão, mover para histórico
            if sessao_id:
                try:
                    comissao_valor = (
                        round(valor * (porcentagem / 100), 2)
                        if porcentagem > 0
                        else 0.0
                    )
                    mover_para_historico(int(sessao_id), valor, comissao_valor)
                except Exception as e:
                    flash("Erro ao mover sessão para histórico.", "erro")

            return redirect(url_for("financeiro_bp.listar_pagamentos"))
        except Exception as e:
            flash("Dados inválidos no formulário.", "erro")

    # GET: Preencher campos do formulário com query string se existirem
    valor_qs = request.args.get("valor", "")
    artista_qs = request.args.get("artista", "")
    porcentagem_qs = request.args.get("porcentagem", "")
    descricao_qs = request.args.get("descricao", "")
    cliente_qs = request.args.get("cliente", "")
    data_qs = request.args.get("data", "")
    forma_pagamento_qs = request.args.get("forma_pagamento", "")
    sessao_id_qs = request.args.get("sessao_id", "")

    # Monta dicionário para o template
    campos_qs = {
        "valor": valor_qs,
        "artista": artista_qs,
        "porcentagem_comissao": porcentagem_qs,
        "descricao": descricao_qs,
        "cliente": cliente_qs,
        "data": data_qs,
        "forma_pagamento": forma_pagamento_qs,
        "sessao_id": sessao_id_qs,
    }

    return render_template(
        "financeiro/registrar_pagamento.html",
        artistas=artistas,
        formas_pagamento=FORMAS_PAGAMENTO,
        campos_qs=campos_qs,
    )


@financeiro_bp.route("/excluir/<int:indice>", methods=["POST", "GET"])
def excluir_pagamento_route(indice):
    from pathlib import Path
    import json

    redirect_hist = request.args.get("redirect_hist")
    caminho = Path(__file__).parent.parent / "dados" / "historico_pagamentos.json"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception:
        pagamentos = []
    if 0 <= indice < len(pagamentos):
        pagamentos.pop(indice)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(pagamentos, f, indent=4, ensure_ascii=False)
        flash("Pagamento excluído com sucesso.", "sucesso")
    else:
        flash("Erro ao excluir pagamento.", "erro")
    if redirect_hist:
        return redirect(url_for("historico_bp.historico_pagamentos"))
    return redirect(url_for("financeiro_bp.listar_pagamentos"))


@financeiro_bp.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar_pagamento(indice):
    from pathlib import Path
    import json

    caminho = Path(__file__).parent.parent / "dados" / "historico_pagamentos.json"
    artistas = carregar_artistas()
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception:
        pagamentos = []

    if indice < 0 or indice >= len(pagamentos):
        flash("Pagamento não encontrado.", "erro")
        return redirect(url_for("financeiro_bp.listar_pagamentos"))

    pagamento = pagamentos[indice]

    if request.method == "POST":
        try:
            # Determina a forma de pagamento final
            forma_pagamento = request.form.get("forma_pagamento")
            outra_forma = request.form.get("outra_forma_pagamento", "").strip()
            forma_final = (
                outra_forma if forma_pagamento == "Outros" else forma_pagamento
            )

            pagamento.update(
                {
                    "data": request.form.get("data"),
                    "cliente": request.form.get("cliente"),
                    "artista": request.form.get("artista"),
                    "valor": float(request.form.get("valor", 0)),
                    "forma_pagamento": forma_final,
                    "descricao": request.form.get("descricao", ""),
                }
            )

            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(pagamentos, f, indent=4, ensure_ascii=False)
            flash("Pagamento atualizado com sucesso!", "sucesso")
            return redirect(url_for("financeiro_bp.listar_pagamentos"))
        except Exception as e:
            flash("Dados inválidos no formulário.", "erro")

    # Prepara os dados para exibição
    forma_exibicao = pagamento["forma_pagamento"]
    outra_forma = ""
    if forma_exibicao not in FORMAS_PAGAMENTO:
        forma_exibicao = "Outros"
        outra_forma = pagamento["forma_pagamento"]

    return render_template(
        "financeiro/editar_pagamento.html",
        pagamento=pagamento,
        indice=indice,
        artistas=artistas,
        formas_pagamento=FORMAS_PAGAMENTO,
        forma_pagamento=forma_exibicao,
        outra_forma_pagamento=outra_forma,
    )
