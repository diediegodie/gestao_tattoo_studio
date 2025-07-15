from flask import Blueprint, render_template, request, redirect, url_for, flash
from financeiro.caixa import (
    carregar_pagamentos,
    registrar_pagamento,
    excluir_pagamento,
    salvar_pagamentos,
    CAMINHO_PAGAMENTOS,
)
from financeiro.comissoes import (
    registrar_comissao_avulsa,
    carregar_comissoes,
    salvar_comissoes,
    gerar_id_comissao,
)
from cadastro_interno.artistas import carregar_artistas
from datetime import datetime
from sessoes.historico import mover_para_historico
from pathlib import Path
import json

financeiro_bp = Blueprint("financeiro_bp", __name__, url_prefix="/financeiro")

FORMAS_PAGAMENTO = ["Dinheiro", "Pix", "Crédito", "Débito", "Outros"]


# Helper functions for loading/saving historical payments/commissions
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


@financeiro_bp.route("/registrar", methods=["GET", "POST"])
def registrar_pagamento_route():
    artistas = carregar_artistas()
    if request.method == "POST":
        try:
            valor_str = request.form.get("valor", "0").replace(",", ".")
            try:
                valor = float(valor_str)
            except Exception:
                valor = 0.0
            artista = request.form.get("artista", "").strip()
            porcentagem_str = request.form.get("porcentagem_comissao", "0").replace(
                ",", "."
            )
            try:
                porcentagem = float(porcentagem_str)
            except Exception:
                porcentagem = 0.0
            descricao = request.form.get("descricao", "").strip()
            data = request.form.get("data") or datetime.now().strftime("%Y-%m-%d")
            cliente = request.form.get("cliente", "").strip()
            forma_pagamento = request.form.get("forma_pagamento", "").strip()
            sessao_id = request.form.get("sessao_id") or request.args.get("sessao_id")

            historico_pagamentos = carregar_historico_pagamentos()
            if historico_pagamentos:
                novo_id = (
                    max(
                        [
                            int(p.get("id", 0))
                            for p in historico_pagamentos
                            if str(p.get("id", "")).isdigit()
                        ]
                        + [0]
                    )
                    + 1
                )
            else:
                novo_id = 1

            novo_pagamento = {
                "id": novo_id,
                "data": data,
                "cliente": cliente,
                "artista": artista,
                "valor": valor,
                "forma_pagamento": forma_pagamento,
                "descricao": descricao,
                "porcentagem_comissao": porcentagem,
            }
            historico_pagamentos.append(novo_pagamento)
            salvar_historico_pagamentos(historico_pagamentos)

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
                    comissoes.append(nova_comissao)
                    salvar_comissoes(comissoes)
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


@financeiro_bp.route("/", methods=["GET"])
def listar_pagamentos():
    caminho = Path(__file__).parent.parent / "dados" / "historico_pagamentos.json"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception:
        pagamentos = []
    # Ensure all pagamentos have an 'id' key for template compatibility
    for idx, p in enumerate(pagamentos):
        if "id" not in p:
            p["id"] = idx
    return render_template(
        "financeiro/financeiro.html",
        pagamentos=pagamentos,
        formas_pagamento=FORMAS_PAGAMENTO,
        filtro_ativo=False,
    )


@financeiro_bp.route("/excluir/<id>", methods=["POST", "GET"])
def excluir_pagamento_route(id):
    from pathlib import Path
    import json

    redirect_hist = request.args.get("redirect_hist")
    caminho = Path(__file__).parent.parent / "dados" / "historico_pagamentos.json"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception:
        pagamentos = []
    idx = next(
        (i for i, p in enumerate(pagamentos) if str(p.get("id")) == str(id)), None
    )
    if idx is not None:
        pagamentos.pop(idx)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(pagamentos, f, indent=4, ensure_ascii=False)
        flash("Pagamento excluído com sucesso.", "sucesso")
    else:
        flash("Erro ao excluir pagamento.", "erro")
    if redirect_hist:
        return redirect(url_for("historico_bp.historico_pagamentos"))
    return redirect(url_for("financeiro_bp.listar_pagamentos"))


@financeiro_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar_pagamento(id):
    from pathlib import Path
    import json

    caminho = Path(__file__).parent.parent / "dados" / "historico_pagamentos.json"
    artistas = carregar_artistas()
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception:
        pagamentos = []

    pagamento = next((p for p in pagamentos if str(p.get("id")) == str(id)), None)
    if not pagamento:
        flash("Pagamento não encontrado.", "erro")
        return redirect(url_for("financeiro_bp.listar_pagamentos"))

    if request.method == "POST":
        try:
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
        id=id,
        artistas=artistas,
        formas_pagamento=FORMAS_PAGAMENTO,
        forma_pagamento=forma_exibicao,
        outra_forma_pagamento=outra_forma,
    )
