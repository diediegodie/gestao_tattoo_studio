from . import historico_bp
from flask import render_template, request, jsonify, flash, redirect, url_for
from pathlib import Path
import json
from datetime import date
from collections import defaultdict


@historico_bp.route("/arquivar_sessoes", methods=["POST"])
def arquivar_sessoes():
    base = Path(__file__).parent.parent / "dados"
    sessoes_path = base / "sessoes.json"
    historico_sessoes_path = base / "historico_sessoes.json"
    backup_dir = base / "historico_antigo"
    backup_dir.mkdir(exist_ok=True)
    # Load all sessions from historico_sessoes.json
    try:
        with open(historico_sessoes_path, "r", encoding="utf-8") as f:
            sessoes_realizadas = json.load(f)
    except Exception:
        sessoes_realizadas = []
    if not sessoes_realizadas:
        flash("Nenhuma sessão realizada para arquivar.", "aviso")
        return redirect(url_for("historico_bp.historico_index"))
    # Group sessions by (year, month)
    sessoes_by_month = defaultdict(list)
    for sessao in sessoes_realizadas:
        try:
            dt = sessao.get("data")
            if dt:
                year, month = dt.split("-")[:2]
                key = (int(year), int(month))
                sessoes_by_month[key].append(sessao)
        except Exception:
            continue
    # For each month, append to backup file
    for (year, month), sessoes_list in sessoes_by_month.items():
        backup_file = backup_dir / f"sessoes_{year}_{int(month):02d}.json"
        if backup_file.exists():
            try:
                with open(backup_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []
            existing.extend(sessoes_list)
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=4, ensure_ascii=False)
        else:
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(sessoes_list, f, indent=4, ensure_ascii=False)
    # Remove archived sessions from historico_sessoes.json
    with open(historico_sessoes_path, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)
    flash("Sessões arquivadas com sucesso.", "sucesso")
    return redirect(url_for("historico_bp.historico_index"))


# Rota para editar comissão por artista
from . import historico_bp
from flask import render_template, request, jsonify, flash, redirect, url_for
from pathlib import Path
import json
from datetime import date


@historico_bp.route("/comissoes/editar/<id>", methods=["GET", "POST"])
def editar_comissao(id):
    base = Path(__file__).parent.parent / "dados"
    caminho = base / "historico_comissoes.json"
    comissoes = []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            comissoes = json.load(f)
    except Exception as e:
        flash("Erro ao carregar dados da comissão.", "erro")
        return redirect(url_for("historico_bp.historico_index"))

    comissao = next((c for c in comissoes if str(c.get("id")) == str(id)), None)
    if not comissao:
        flash("Comissão não encontrada.", "erro")
        return redirect(url_for("historico_bp.historico_index"))

    if request.method == "POST":
        try:
            nova_comissao = float(
                request.form.get("comissao", comissao.get("porcentagem", 0))
            )
            comissao["porcentagem"] = nova_comissao
            valor_total = comissao.get("valor_total")
            if valor_total is not None:
                try:
                    valor_total = float(valor_total)
                    comissao["valor_comissao"] = round(
                        valor_total * (nova_comissao / 100), 2
                    )
                except Exception:
                    pass
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(comissoes, f, indent=4, ensure_ascii=False)
            flash("Comissão atualizada com sucesso!", "sucesso")
            return redirect(url_for("historico_bp.historico_index"))
        except Exception as e:
            flash("Erro ao salvar alterações.", "erro")

    return render_template(
        "historico/editar_comissao.html", artista=comissao["artista"], comissao=comissao
    )


@historico_bp.route("/")
def historico_index():
    base = Path(__file__).parent.parent / "dados"
    # Pagamentos
    pagamentos = []
    pagamentos_path = base / "historico_pagamentos.json"
    try:
        with open(pagamentos_path, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception:
        pass
    # Ensure all pagamentos have a unique, persistent 'id' key
    import uuid

    changed = False
    existing_ids = set()
    for p in pagamentos:
        if "id" in p:
            existing_ids.add(str(p["id"]))
    for p in pagamentos:
        if (
            "id" not in p
            or str(p["id"]) in (None, "", "null")
            or list(existing_ids).count(str(p["id"])) > 1
        ):
            new_id = str(uuid.uuid4())
            while new_id in existing_ids:
                new_id = str(uuid.uuid4())
            p["id"] = new_id
            existing_ids.add(new_id)
            changed = True
    if changed:
        with open(pagamentos_path, "w", encoding="utf-8") as f:
            json.dump(pagamentos, f, indent=4, ensure_ascii=False)

    # Ensure all comissoes have a unique, persistent 'id' key
    comissoes = []
    comissoes_path = base / "historico_comissoes.json"
    try:
        with open(comissoes_path, "r", encoding="utf-8") as f:
            comissoes = json.load(f)
    except Exception:
        pass
    changed_comissoes = False
    existing_com_ids = set()
    for c in comissoes:
        if "id" in c:
            existing_com_ids.add(str(c["id"]))
    for c in comissoes:
        if (
            "id" not in c
            or str(c["id"]) in (None, "", "null")
            or list(existing_com_ids).count(str(c["id"])) > 1
        ):
            new_id = str(uuid.uuid4())
            while new_id in existing_com_ids:
                new_id = str(uuid.uuid4())
            c["id"] = new_id
            existing_com_ids.add(new_id)
            changed_comissoes = True
    if changed_comissoes:
        with open(comissoes_path, "w", encoding="utf-8") as f:
            json.dump(comissoes, f, indent=4, ensure_ascii=False)
    pagamentos = list(reversed(pagamentos))
    # Use the comissoes list with guaranteed ids
    # (already loaded and fixed above)
    comissoes = list(reversed(comissoes))
    # Sessões realizadas
    sessoes = []
    try:
        caminho_sessoes = base / "historico_sessoes.json"
        with open(caminho_sessoes, "r", encoding="utf-8") as f:
            sessoes = json.load(f)
    except Exception:
        pass
    # Ensure all sessoes have an 'id' key for template compatibility
    sessoes = list(reversed(sessoes))
    for idx, s in enumerate(sessoes):
        if "id" not in s:
            s["id"] = idx
    return render_template(
        "historico/historico.html",
        pagamentos=pagamentos,
        comissoes=comissoes,
        sessoes=sessoes,
    )


@historico_bp.route("/pagamentos")
def historico_pagamentos():
    base = Path(__file__).parent.parent / "dados"
    pagamentos = []
    try:
        with open(base / "historico_pagamentos.json", "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception as e:
        pass
    return render_template("historico/pagamentos.html", pagamentos=pagamentos)


@historico_bp.route("/comissoes")
def historico_comissoes():
    base = Path(__file__).parent.parent / "dados"
    comissoes = []
    try:
        with open(base / "historico_comissoes.json", "r", encoding="utf-8") as f:
            comissoes = json.load(f)
    except Exception as e:
        pass
    return render_template("historico/comissoes.html", comissoes=comissoes)


@historico_bp.route("/sessoes/excluir/<int:id>", methods=["POST"])
def excluir_sessao_realizada(id):
    base = Path(__file__).parent.parent / "dados"
    caminho_sessoes = base / "historico_sessoes.json"
    sessoes = []
    try:
        with open(caminho_sessoes, "r", encoding="utf-8") as f:
            sessoes = json.load(f)
    except Exception:
        pass
    sessoes = [s for s in sessoes if int(s.get("id", -1)) != int(id)]
    with open(caminho_sessoes, "w", encoding="utf-8") as f:
        json.dump(sessoes, f, indent=4, ensure_ascii=False)
    flash("Sessão removida do histórico com sucesso!", "sucesso")
    return redirect(url_for("historico_bp.historico_index"))


@historico_bp.route("/pagamentos/excluir/<id>", methods=["POST"])
def excluir_pagamento_historico(id):
    base = Path(__file__).parent.parent / "dados"
    caminho = base / "historico_pagamentos.json"
    pagamentos = []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            pagamentos = json.load(f)
    except Exception:
        pass
    # Remove pagamento by id (string match)
    original_len = len(pagamentos)
    pagamentos = [p for p in pagamentos if str(p.get("id")) != str(id)]
    if len(pagamentos) < original_len:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(pagamentos, f, indent=4, ensure_ascii=False)
        flash("Pagamento excluído com sucesso.", "sucesso")
    else:
        flash("Erro ao excluir pagamento.", "erro")
    return redirect(url_for("historico_bp.historico_index"))


@historico_bp.route("/comissoes/excluir/<int:indice>", methods=["POST"])
def excluir_comissao_historico(indice):
    base = Path(__file__).parent.parent / "dados"
    caminho = base / "historico_comissoes.json"
    comissoes = []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            comissoes = json.load(f)
    except Exception:
        pass
    if 0 <= indice < len(comissoes):
        comissoes.pop(indice)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(comissoes, f, indent=4, ensure_ascii=False)
        flash("Comissão excluída com sucesso.", "sucesso")
    else:
        flash("Erro ao excluir comissão.", "erro")
    return redirect(url_for("historico_bp.historico_index"))


@historico_bp.route("/sessoes/editar/<int:id>", methods=["GET", "POST"])
def editar_historico(id):
    base = Path(__file__).parent.parent / "dados"
    caminho_sessoes = base / "historico_sessoes.json"
    sessoes = []
    try:
        with open(caminho_sessoes, "r", encoding="utf-8") as f:
            sessoes = json.load(f)
    except Exception as e:
        flash("Erro ao carregar dados da sessão.", "erro")
        return redirect(url_for("historico_bp.historico_index"))

    sessao = next((s for s in sessoes if int(s.get("id", -1)) == int(id)), None)
    if not sessao:
        flash("Sessão não encontrada.", "erro")
        return redirect(url_for("historico_bp.historico_index"))

    if request.method == "POST":
        valor = request.form.get("valor", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        # Só valida os campos que são editáveis
        erros = []
        if valor == "":
            erros.append("Valor é obrigatório.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template("historico/editar.html", sessao=sessao)

        # Atualiza apenas os campos editáveis
        sessao["valor"] = float(valor) if valor else 0.0
        sessao["observacoes"] = observacoes

        # Salva as alterações
        try:
            with open(caminho_sessoes, "w", encoding="utf-8") as f:
                json.dump(sessoes, f, indent=4, ensure_ascii=False)
            flash("Sessão atualizada com sucesso!", "sucesso")
            return redirect(url_for("historico_bp.historico_index"))
        except Exception as e:
            flash("Erro ao salvar alterações.", "erro")
            return render_template("historico/editar.html", sessao=sessao)

    return render_template("historico/editar.html", sessao=sessao)
