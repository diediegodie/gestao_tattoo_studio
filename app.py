from flask import Flask, render_template
from estoque.views import estoque_bp
from financeiro.routes import financeiro_bp
from sessoes.routes import sessoes_bp
from financeiro.extrato import extrato_bp
from datetime import datetime

app = Flask(__name__)
app.secret_key = "1234"


# Filtro personalizado para exibir datas no formato brasileiro
@app.template_filter("data_brasileira")
def data_brasileira(data_str):
    try:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d")
        return data_obj.strftime("%d/%m/%Y")
    except:
        return data_str


# Registro dos blueprints
app.register_blueprint(estoque_bp)
app.register_blueprint(financeiro_bp)
app.register_blueprint(sessoes_bp)
app.register_blueprint(extrato_bp)


@app.route("/")
def index():
    return render_template("index.html")
