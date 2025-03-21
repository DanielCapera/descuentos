from flask import Flask, render_template, jsonify, request
from auth import obtener_access_token
import requests
import urllib.parse  # Para codificar/decodificar datos en la URL

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["TEMPLATES_AUTO_RELOAD"] = True

ACCESS_TOKEN = obtener_access_token()
if not ACCESS_TOKEN:
    print("❌ No se pudo obtener el Access Token. Verifica las credenciales.")
    exit()  # Sale del programa si no se puede obtener el token

SITE_ID = "MCO"  # Código del sitio (Colombia)
QUERY = "computadores lenovo"  # Palabra clave de búsqueda

def obtener_productos():
    url = f"https://api.mercadolibre.com/sites/{SITE_ID}/search?q={QUERY}&limit=9"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        productos = []
        
        for item in data["results"]:
            # Obtener una imagen más grande si está disponible
            image_url = item["thumbnail"].replace("I.jpg", "O.jpg")  # Imagen en mejor calidad

            productos.append({
                "titulo": item["title"],
                "precio": item["price"],
                "link": item["permalink"],
                "imagen": image_url
            })
        
        return productos
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def format_price(value):
    """Formatea el precio con separadores de miles y símbolo de pesos."""
    try:
        return "${:,.0f}".format(float(value)).replace(",", ".")
    except ValueError:
        return value  # Si el valor no es convertible, se devuelve tal cual

# Registrar el filtro en Jinja2
app.jinja_env.filters["format_price"] = format_price

@app.route('/')
def home():
    productos = obtener_productos()
    return render_template('index.html', productos=productos)

@app.route('/producto')
def detalle_producto():
    """Recibe los datos desde la URL y los pasa a detalle.html"""
    titulo = request.args.get("titulo")
    precio = request.args.get("precio")
    imagen = request.args.get("imagen")

    if not titulo or not precio or not imagen:
        return "Producto no encontrado", 404

    return render_template('detalle.html', titulo=titulo, precio=precio, imagen=imagen)

@app.route('/api/productos')
def api_productos():
    productos = obtener_productos()
    return jsonify(productos)

if __name__ == '__main__':
    app.run(debug=True)
