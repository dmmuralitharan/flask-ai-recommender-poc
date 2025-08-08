from datetime import datetime, timezone
import os
from flask import jsonify, request
from src import db
from src.models.product_model import Product
from src.utils.file_upload import save__file


def create_product_controller():
    try:
        data = request.form
        print(data)
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        price = float(price)
        category = data.get("category")
        stock_quantity = data.get("stock_quantity", 0)
        stock_quantity = int(stock_quantity)
        is_active = data.get("is_active", True)

        new_product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            stock_quantity=stock_quantity,
            is_active=is_active,
        )

        db.session.add(new_product)
        db.session.flush()
        print("1")
        product_file = request.files.get("product_file")

        if product_file:
            new_product.image_url = save__file(
                product_file, "product", "image", new_product.id, 1, 3
            )

        db.session.commit()

        return (
            jsonify(
                {
                    "status": 1,
                    "msg": "Product added successfully",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": 0, "error": str(e)}), 500


def get_all_products_controller():
    try:
        products = Product.query.order_by(Product.created_at.desc()).all()
        product_list = [product.to_dict() for product in products]

        return (
            jsonify({"status": 1, "data": product_list, "count": len(product_list)}),
            200,
        )

    except Exception as e:
        return jsonify({"status": 0, "error": str(e)}), 500


def get_product_controller(product_id):
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"status": 0, "msg": "Product not found"}), 404

        return jsonify({"status": 1, "data": product.to_dict()}), 200

    except Exception as e:
        return jsonify({"status": 0, "error": str(e)}), 500


def update_product_controller(product_id):
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"status": 0, "msg": "Product not found"}), 404

        data = request.form

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.category = data.get("category", product.category)
        product.stock_quantity = data.get("stock_quantity", product.stock_quantity)
        product.is_active = data.get("is_active", product.is_active)
        product.updated_at = datetime.now(timezone.utc)

        db.session.commit()

        product_file = request.files.get("product_file")

        if product_file:
            if product.image_url and os.path.exists(product.image_url):
                os.remove(product.image_url)

            product.image_url = save__file(
                product_file, "product", "image", product.id, 1, 3
            )
        db.session.commit()

        return (
            jsonify(
                {
                    "status": 1,
                    "msg": "Product updated successfully",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": 0, "error": str(e)}), 500


def delete_product_controller(product_id):
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"status": 0, "msg": "Product not found"}), 404
        
        if product.image_url and os.path.exists(product.image_url):
            os.remove(product.image_url)

        db.session.commit()

        db.session.delete(product)
        db.session.commit()

        return jsonify({"status": 1, "msg": "Product deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": 0, "error": str(e)}), 500
