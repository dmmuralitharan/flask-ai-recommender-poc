from flask import Blueprint
from src.controllers.product_controller import (
    create_product_controller,
    delete_product_controller,
    get_all_products_controller,
    get_product_controller,
    recommend_products_from_search_controller,
    search_product_controller,
    update_product_controller,
)

product_bp = Blueprint("product", __name__, url_prefix="/api/v1/products")


@product_bp.route("/", methods=["POST"])
def create_product():
    return create_product_controller()


@product_bp.route("/", methods=["GET"])
def get_all_products():
    return get_all_products_controller()


@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    return get_product_controller(id)


@product_bp.route("/<int:id>", methods=["PUT"])
def update_product(id):
    return update_product_controller(id)


@product_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    return delete_product_controller(id)

@product_bp.route("/search", methods=["GET"])
def search_product():
    return search_product_controller()

@product_bp.route("/recommend_products", methods=["GET"])
def recommend_products_from_search():
    return recommend_products_from_search_controller()
