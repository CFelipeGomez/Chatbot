from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_model import analizar_texto, extraer_entidades, limpiar_texto
from recommender import recomendar_auto

app = Flask(__name__)
CORS(app)

# 🔹 Guardamos contexto en memoria simple (para demo). 
# En producción lo mejor es usar sesiones o base de datos.
contexto_global = {}

@app.route("/chat", methods=["POST"])
def chat():
    global contexto_global
    data = request.get_json()
    mensaje_usuario = data.get("message", "").strip()

    if not mensaje_usuario:
        return jsonify({"response": "Por favor escribe algo sobre el auto que buscas."})

    # Procesar con NLP
    tokens = analizar_texto(mensaje_usuario)
    entidades = extraer_entidades(mensaje_usuario)
    lemas = limpiar_texto(mensaje_usuario)

    # ✅ Ahora sí recibimos (respuesta, contexto)
    respuesta, contexto_global = recomendar_auto(mensaje_usuario, tokens, contexto_global)

    return jsonify({
        "response": respuesta,   # solo el texto
        "debug": {
            "tokens": tokens,
            "entidades": entidades,
            "lemas": lemas,
            "contexto": contexto_global
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
