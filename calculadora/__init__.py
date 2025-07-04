from flask import Blueprint

calculadora_bp = Blueprint('calculadora_bp', __name__, url_prefix='/calculadora')

from . import routes  # Importação relativa