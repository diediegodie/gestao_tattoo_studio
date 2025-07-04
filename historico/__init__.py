from flask import Blueprint

historico_bp = Blueprint('historico_bp', __name__, url_prefix='/historico')

from . import routes
