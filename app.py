from flask import Flask, render_template
from estoque.views import estoque_bp
from financeiro.routes import financeiro_bp
from sessoes.routes import sessoes_bp
from financeiro.extrato import extrato_bp

app = Flask(__name__)
app.secret_key = "1234"

app.register_blueprint(estoque_bp)
app.register_blueprint(financeiro_bp)
app.register_blueprint(sessoes_bp)
app.register_blueprint(extrato_bp)

@app.route("/")
def index():
    return render_template("index.html")
