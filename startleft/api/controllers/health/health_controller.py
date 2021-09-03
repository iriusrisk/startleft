from flask import Blueprint

bp = Blueprint("health", __name__, url_prefix="")


@bp.route('/health')
def hello_world():
    return "<p>StartLeft server is ok</p>"
