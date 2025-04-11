# Preguntas y Respuestas para Sustentación de Proyecto de Tesis

## 🧠 Preguntas Técnicas

**1. ¿Por qué elegiste MongoDB en lugar de una base de datos relacional como MySQL o PostgreSQL?**  
Porque MongoDB permite almacenar documentos flexibles con estructuras anidadas, lo que facilita el manejo de datos de productos que pueden variar según la tienda (nombre, precio, URL, fecha, etc.) sin necesidad de normalización rígida.

**2. ¿Cómo se entrena el modelo de machine learning y qué algoritmo utilizaste?**  
Se entrenó un modelo supervisado usando `scikit-learn`, específicamente un clasificador como Random Forest, con datos históricos de precios. El modelo aprende a diferenciar patrones reales de descuento frente a precios inflados.

**3. ¿Cómo aseguras que los datos recolectados son confiables para el entrenamiento del modelo?**  
Se realiza un preprocesamiento que incluye limpieza, verificación de campos clave (precio, fecha, nombre) y comparación cruzada entre múltiples tiendas para evitar inconsistencias.

**4. ¿Por qué usaste `joblib` en lugar de `pickle` para guardar el modelo?**  
Porque `joblib` es más eficiente para serializar modelos grandes de scikit-learn, especialmente cuando contienen estructuras de datos como arrays de `numpy`.

---

## 💡 Preguntas de Lógica del Proyecto

**6. ¿Cómo identifica tu sistema si una promoción es engañosa o no?**  
Compara el precio actual con el histórico en un periodo razonable y evalúa si hay una subida previa al descuento. El modelo predice si el patrón es típico de promociones reales o manipuladas.

**7. ¿Qué problema específico estás resolviendo con este proyecto?**  
La desinformación sobre descuentos reales en tiendas online. Muchos usuarios no saben si un descuento es verdadero o inflado. Mi herramienta permite detectar y alertar sobre estas prácticas.

**8. ¿Cuál fue tu motivación principal para desarrollar este sistema?**  
Como consumidor, he notado prácticas engañosas en promociones. Quise construir una solución que use inteligencia artificial para empoderar al usuario y brindar transparencia en los precios.

**9. ¿Cuál fue el mayor reto técnico que enfrentaste y cómo lo resolviste?**  
Integrar el modelo entrenado con la aplicación web sin afectar el rendimiento. Lo resolví usando `joblib` para cargar el modelo en tiempo de ejecución y evitar reentrenamiento continuo.

**10. ¿Este sistema puede adaptarse a distintos productos o tipos de tienda?**  
Sí. Gracias al uso de scraping flexible y almacenamiento en MongoDB, el sistema puede adaptarse fácilmente a diferentes estructuras de datos según el comercio.

---

## 🔐 Preguntas de Seguridad y Ética

**12. ¿Podría este sistema usarse para perjudicar a tiendas en línea?**  
No es el objetivo. Está diseñado para informar al usuario y promover la transparencia. No se publica información sensible ni se afecta directamente el funcionamiento de ninguna tienda.

---

## 📈 Preguntas sobre Resultados y Validación

**13. ¿Cómo validaste que tu modelo funciona correctamente?**  
Se dividió el dataset en entrenamiento y prueba. Se aplicó validación cruzada y métricas como precisión, recall para evaluar el rendimiento. El modelo superó el 85% de precisión en la detección de descuentos reales vs. engañosos.

**14. ¿Qué pasaría si una tienda cambia su estrategia de precios? ¿El modelo seguiría siendo útil?**  
El sistema está diseñado para adaptarse: al seguir recolectando nuevos datos, se puede reentrenar periódicamente para mantenerse actualizado ante cambios en las dinámicas del mercado.

**15. ¿Se puede implementar esto como una extensión de navegador o app móvil?**  
Sí, en el futuro se podría crear una extensión que muestre la veracidad del descuento directamente en la página del producto, o una app que alerte al usuario sobre promociones reales.

---
