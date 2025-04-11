from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from predictor import predecir_descuento

app = Flask(__name__, template_folder="templates", static_folder="static")

# Conexión a MongoDB
MONGO_URI = "mongodb+srv://descuentos:Descuentos@cluster0.zdyuqgy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["descuentos"]
collection = db["computadores"]

def format_price(value):
    """Formatea el precio con separadores de miles y símbolo de pesos."""
    try:
        return "${:,.0f}".format(float(value)).replace(",", ".")
    except ValueError:
        return value

app.jinja_env.filters["format_price"] = format_price

@app.route("/")
def home():
    productos = list(collection.find({}, {"_id": 0, "modelo": 1, "descripcion": 1, "precio_actual": 1, "imagen": 1}).limit(9))
    return render_template("index.html", productos=productos)

@app.route("/detalle/<descripcion>")
def detalle_producto(descripcion):
    producto = collection.find_one(
        {"descripcion": descripcion},
        {
            "_id": 0,
            "descripcion": 1,
            "precio_actual": 1,
            "imagen": 1,
            "modelo": 1,
            "url": 1,
            "datos_web_uno": 1,
            "datos_web_dos": 1,
            "historico_precios": 1
        }
    )

    if not producto:
        return "Producto no encontrado", 404
    
    es_descuento_real = predecir_descuento(producto)

    return render_template(
        "detalle.html",
        titulo=producto["descripcion"],
        precio=producto["precio_actual"],
        imagen=producto["imagen"],
        url=producto["url"],
        web_uno=producto.get("datos_web_uno"),
        web_dos=producto.get("datos_web_dos"),
        historico_precios=producto.get("historico_precios"),
        es_descuento_real=es_descuento_real
    )
    
@app.route("/load_more", methods=["POST"])
def load_more():
    skip = int(request.json.get("skip", 0))
    per_page = 9

    productos_cursor = collection.find(
        {},
        {"_id": 0, "modelo": 1, "descripcion": 1, "precio_actual": 1, "imagen": 1}
    ).skip(skip).limit(per_page)

    productos = list(productos_cursor)

    return jsonify({
        "productos": productos,
        "has_more": collection.count_documents({}) > skip + per_page
    })
if __name__ == "__main__":
    app.run(debug=True)
