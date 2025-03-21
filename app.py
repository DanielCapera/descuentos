from flask import Flask, render_template, request, jsonify
from config import db

app = Flask(__name__)

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# API para obtener productos desde MongoDB
@app.route("/api/products")
def get_products():
    products = list(db.products.find({}, {"_id": 0}))  # No incluimos _id
    return jsonify(products)

# API para agregar productos
@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.json
    db.products.insert_one(data)
    return jsonify({"message": "Producto agregado"}), 201

if __name__ == "__main__":
    app.run(debug=True)
