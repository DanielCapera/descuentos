import pandas as pd
import joblib
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Conexión a MongoDB
MONGO_URI = "mongodb+srv://descuentos:Descuentos@cluster0.zdyuqgy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["descuentos"]
collection = db["computadores"]

# Obtener los datos
productos = list(collection.find())

# Inicializar contadores y dataset
descartados = {
    "sin_historico": 0,
    "historico_malformado": 0,
    "pocos_precios_validos": 0,
    "precio_actual_invalido": 0,
    "error_desconocido": 0
}
datos = []

for p in productos:
    try:
        historico = p.get("historico_precios", {})

        historico_validado = []
        if isinstance(historico, dict):
            historico_validado = [precio for precio in historico.values() if isinstance(precio, (int, float))]
        elif isinstance(historico, list):
            historico_validado = [h["precio"] for h in historico if isinstance(h, dict) and "precio" in h and isinstance(h["precio"], (int, float))]
        else:
            descartados["historico_malformado"] += 1
            continue

        if len(historico_validado) < 2:
            descartados["pocos_precios_validos"] += 1
            continue

        precio_actual = p.get("precio_actual")
        if precio_actual is None or not isinstance(precio_actual, (int, float)):
            descartados["precio_actual_invalido"] += 1
            continue

        precio_minimo = min(historico_validado)
        precio_maximo = max(historico_validado)
        promedio = sum(historico_validado) / len(historico_validado)

        es_descuento_real = precio_actual <= 0.9 * promedio

        datos.append({
            "precio_actual": precio_actual,
            "precio_minimo": precio_minimo,
            "precio_maximo": precio_maximo,
            "precio_promedio": promedio,
            "es_descuento_real": int(es_descuento_real)
        })

    except Exception as e:
        descartados["error_desconocido"] += 1
        print(f"⚠️ Error con producto: {e}")
        continue

print("🔍 Productos válidos para entrenamiento:", len(datos))

# Crear DataFrame
df = pd.DataFrame(datos)

# Validar que se obtuvieron datos
if df.empty:
    print("❌ No se pudo entrenar el modelo porque no se encontraron datos válidos.")
else:
    # Entrenar modelo
    X = df[["precio_actual", "precio_minimo", "precio_maximo", "precio_promedio"]]
    y = df["es_descuento_real"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Guardar modelo
    joblib.dump(modelo, "modelo_descuentos.pkl")
    print("✅ Modelo entrenado y guardado en modelo_descuentos.pkl")

# Cargar el modelo entrenado
modelo = joblib.load("modelo_descuentos.pkl")

print("\n📊 Predicciones para productos actuales:")

# Recorrer los productos otra vez para predecir con el modelo
for i, p in enumerate(productos):
    try:
        historico = p.get("historico_precios", {})

        # Validar histórico como antes
        historico_validado = []
        if isinstance(historico, dict):
            historico_validado = [precio for precio in historico.values() if isinstance(precio, (int, float))]
        elif isinstance(historico, list):
            historico_validado = [h["precio"] for h in historico if isinstance(h, dict) and "precio" in h and isinstance(h["precio"], (int, float))]
        else:
            continue

        if len(historico_validado) < 2:
            continue

        precio_actual = p.get("precio_actual")
        if precio_actual is None or not isinstance(precio_actual, (int, float)):
            continue

        precio_minimo = min(historico_validado)
        precio_maximo = max(historico_validado)
        promedio = sum(historico_validado) / len(historico_validado)

        entrada = [[precio_actual, precio_minimo, precio_maximo, promedio]]
        prediccion = modelo.predict(entrada)

        print(f"\n🧾 Producto #{i + 1}")
        print(f"🔸 Precio actual: ${precio_actual}")
        print(f"🔸 Precio promedio: ${promedio:.2f}")
        print(f"🔸 Descuento real: {'✅ Sí' if prediccion[0] == 1 else '❌ No'}")

    except Exception as e:
        print(f"⚠️ Error al predecir producto #{i + 1}: {e}")
