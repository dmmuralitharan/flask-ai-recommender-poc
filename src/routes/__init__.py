from src.routes.auth_route import auth_bp
from src.routes.product_route import product_bp


def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
