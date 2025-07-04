from flask import render_template, request
from historico import historico_bp  # Importa o blueprint já criado
import json
from pathlib import Path

@historico_bp.route("/sessoes", methods=["GET", "POST"])
def historico_sessoes():
    if request.method == "POST":
        # Processar confirmação de fechamento de sessão
        pass
    
    with open(Path(__file__).parent.parent / "dados" / "sessoes.json", 'r', encoding='utf-8') as f:
        dados = json.load(f)
    return render_template("historico/sessoes.html", sessoes=dados['historico'])

@historico_bp.route("/pagamentos")
def historico_pagamentos():
    return render_template("historico/pagamentos.html")