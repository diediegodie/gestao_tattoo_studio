from flask import Flask, render_template
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime  # Necessário para o filtro de data
from calculadora import calculadora_bp

# Forçar importação das rotas do histórico antes de registrar o blueprint
import historico.routes
from historico import historico_bp

# Configuração inicial
load_dotenv()
BASE_DIR = Path(__file__).parent


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

# Executa backup mensal automaticamente no início do app, se for dia 1
from utils.backup_mensal import realizar_backup_mensal
from datetime import datetime

if datetime.now().day == 1:
    realizar_backup_mensal()


# Filtro personalizado para datas
@app.template_filter("data_brasileira")
def data_brasileira(data_str):
    try:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d")
        return data_obj.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return data_str


# Registro de Blueprints
from estoque.views import estoque_bp
from financeiro.routes import financeiro_bp
from sessoes.routes import sessoes_bp
from financeiro.extrato import extrato_bp
from cadastro_interno.routes import cadastro_bp

app.register_blueprint(estoque_bp)
app.register_blueprint(financeiro_bp)
app.register_blueprint(sessoes_bp)
app.register_blueprint(extrato_bp)
app.register_blueprint(cadastro_bp)
app.register_blueprint(calculadora_bp)
app.register_blueprint(historico_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
