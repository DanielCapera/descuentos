from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

# Función para hacer scraping de productos en Mercado Libre
def obtener_productos():
    url = "https://listado.mercadolibre.com.co/computadores-lenovo"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    productos = []
    for item in soup.select(".ui-search-result__content-wrapper")[:10]:
        titulo = item.select_one(".ui-search-item__title").text
        precio = item.select_one(".price-tag-fraction").text
        link = item.select_one("a.ui-search-link")["href"]
        
        productos.append({
            "titulo": titulo,
            "precio": precio,
            "link": link
        })
    
    return productos

# Función para predecir descuento con IA (simulación con random)
def predecir_descuento():
    return round(random.uniform(5, 30), 2)  # Descuento aleatorio entre 5% y 30%

@app.route('/')
def home():
    productos = obtener_productos()
    return render_template('index.html', productos=productos)

@app.route('/producto')
def producto():
    titulo = request.args.get('titulo')
    precio = request.args.get('precio')
    descuento_futuro = predecir_descuento()
    precio_futuro = round(float(precio.replace(',', '')) * (1 - descuento_futuro / 100), 2)
    
    return render_template('producto.html', titulo=titulo, precio=precio, descuento_futuro=descuento_futuro, precio_futuro=precio_futuro)

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

if __name__ == '__main__':
    app.run(debug=True)
