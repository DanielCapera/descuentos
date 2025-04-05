import joblib
import numpy as np

# Cargar modelo (esto se hace una sola vez al importar)
modelo = joblib.load("modelo_descuentos.pkl")

def predecir_descuento(producto):
    historico = producto.get("historico_precios", [])
    if not historico:
        return False  # No se puede predecir sin datos históricos

    try:
        precio_actual = producto.get("precio_actual", 0)

        # Validar precios históricos correctamente
        precios = []
        if isinstance(historico, list):
            precios = [h["precio"] for h in historico if isinstance(h, dict) and "precio" in h and isinstance(h["precio"], (int, float))]
        elif isinstance(historico, dict):
            precios = [v for v in historico.values() if isinstance(v, (int, float))]
        else:
            return False  # Estructura no compatible

        if len(precios) < 2:
            return False  # No hay suficientes datos para predecir

        precio_minimo = min(precios)
        precio_maximo = max(precios)
        precio_promedio = sum(precios) / len(precios)

        features = np.array([[precio_actual, precio_minimo, precio_maximo, precio_promedio]])
        prediccion = modelo.predict(features)

        return bool(prediccion[0])
    except Exception as e:
        print(f"❌ Error en la predicción: {e}")
        return False
