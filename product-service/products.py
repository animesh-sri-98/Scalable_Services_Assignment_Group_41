from flask import Flask, request, jsonify
import random
from pymongo import MongoClient

app = Flask(__name__)
print("connecting to mongodb server")
client = MongoClient("mongodb://mongodb-service:27017/")
db = client["products_db"]
collection = db["products"]

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product_name = data.get('product_name')
    price = data.get('price')

    # Validate input fields
    if not product_name or not isinstance(price, (int, float)):
        return jsonify({"message": "Invalid input data"}), 400

    # Generate a random 3-digit product_id
    product_id = random.randint(100, 999)
    product_data = {
        "product_id": product_id,
        "product_name": product_name,
        "price": price
    }
    collection.insert_one(product_data)

    response = {
        "message": "Product created successfully",
        "product_id": product_id
    }
    return jsonify(response), 201

@app.route('/products', methods=['GET'])
def get_all_products():
    products = list(collection.find({}, {"_id": 0}))
    return jsonify(products), 200

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product_name = data.get('product_name')
    price = data.get('price')

    # Validate input fields
    if not product_name or not isinstance(price, (int, float)):
        return jsonify({"message": "Invalid input data"}), 400

    # Update product details based on product_id
    result = collection.update_one(
        {"product_id": product_id},
        {"$set": {"product_name": product_name, "price": price}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Product updated successfully"}), 200
    else:
        # Product not found, return 404 response
        return jsonify({"message": "Product not found"}), 404


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Retrieve product details based on product_id from MongoDB
    product = collection.find_one({"product_id": product_id})

    if product:
        response = {
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "price": product["price"]
        }
        return jsonify(response), 200
    else:
        # Product not found, return 404 response
        return jsonify({"message": "Product not found"}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Delete product based on product_id from MongoDB
    result = collection.delete_one({"product_id": product_id})

    if result.deleted_count > 0:
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        # Product not found, return 404 response
        return jsonify({"message": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9996)
