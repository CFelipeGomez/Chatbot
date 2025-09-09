# recommender.py mejorado
"""
Módulo de recomendación conversacional.
Devuelve (respuesta_texto_HTML, contexto_actualizado).
"""

import re
import datetime
from typing import Optional, Any, Dict

# ---------------------------
# Base de datos ligera (ejemplos)
# ---------------------------
MODEL_DB = {
    "suv": [
        ("Mazda CX-30", 120_000_000, 180_000_000),
        ("Hyundai Tucson", 130_000_000, 200_000_000),
    ],
    "compacto": [
        ("Chevrolet Onix", 50_000_000, 90_000_000),
        ("Kia Picanto", 40_000_000, 70_000_000),
    ],
    "minivan": [
        ("Kia Carnival", 180_000_000, 260_000_000),
        ("Toyota Sienna", 220_000_000, 320_000_000),
    ],
    "pickup": [
        ("Toyota Hilux", 150_000_000, 260_000_000),
        ("Ford Ranger", 160_000_000, 260_000_000),
    ],
    "clasico": [
        ("Volkswagen Escarabajo", 20_000_000, 50_000_000),
        ("Chevrolet Bel Air", 70_000_000, 200_000_000),
    ],
}

# Consumo ficticio
CONSUMO_ESTIMADO = {"Mazda CX-30": "11-14 km/l", "Chevrolet Onix": "13-17 km/l"}

# Mantenimiento ficticio
MANTENIMIENTO_ESTIMADO = {"Mazda CX-30": "≈ 4-6 millones COP/año", "Chevrolet Onix": "≈ 2-3 millones COP/año"}

# ---------------------------
# Keywords extendidos
# ---------------------------
KEYWORDS = {
    "suv": ["suv", "camioneta", "camionetas"],
    "compacto": ["compacto", "pequeño", "citycar"],
    "minivan": ["minivan", "van", "familiar grande"],
    "pickup": ["pickup", "camioneta de carga", "doble cabina"],
    "clasico": ["clásico", "antiguo", "vintage"],
}

COLOR_KEYWORDS = ["rojo", "negro", "blanco", "azul", "gris", "plateado"]

USO_KEYWORDS = {
    "ciudad": ["ciudad", "urbano", "tráfico"],
    "carretera": ["carretera", "viajes largos", "pueblo"],
    "escolar": ["colegio", "niños", "escolar"],
}

SALUDOS = ["hola", "buenos días", "buenos dias", "buenas tardes", "buenas noches"]

# ---------------------------
# Helpers
# ---------------------------
def obtener_saludo() -> str:
    hora = datetime.datetime.now().hour
    if hora < 12:
        return "☀️ ¡Buenos días!"
    elif 12 <= hora < 18:
        return "🌤️ ¡Buenas tardes!"
    else:
        return "🌙 ¡Buenas noches!"

def es_saludo(mensaje: str) -> bool:
    return any(s in (mensaje or "").lower() for s in SALUDOS)

def detectar_color(mensaje: str) -> Optional[str]:
    for c in COLOR_KEYWORDS:
        if c in mensaje.lower():
            return c
    return None

def detectar_categoria(mensaje: str) -> Optional[str]:
    for cat, kws in KEYWORDS.items():
        if any(k in mensaje.lower() for k in kws):
            return cat
    return None

def buscar_modelos_por_categoria(categoria: str):
    return MODEL_DB.get(categoria, [])

def formato_modelos_para_texto(modelos):
    return "<ul>" + "".join(f"<li>{m} ({low:,d} - {high:,d} COP)</li>" for m, low, high in modelos) + "</ul>"

# ---------------------------
# Motor principal
# ---------------------------
def recomendar_auto(mensaje: str, tokens=None, contexto: Optional[Dict[str, Any]] = None):
    if contexto is None:
        contexto = {}
    mensaje = (mensaje or "").strip()
    nombre = contexto.get("nombre", "amigo")

    # Contador de entradas sin intención
    contexto["nonsense_count"] = contexto.get("nonsense_count", 0)

    # 1) Saludo
    if not contexto.get("saludado", False):
        if es_saludo(mensaje):
            contexto["saludado"] = True
            contexto["esperando_nombre"] = True
            return f"{obtener_saludo()} Soy tu asesor virtual de autos 🚗.<br><br>¿Cómo te llamas?", contexto
        return ("🙋‍♂️ Antes de empezar, por favor salúdame con <b>hola</b>, <b>buenos días</b>, <b>buenas tardes</b> o <b>buenas noches</b>."), contexto

    # 2) Nombre
    if contexto.get("esperando_nombre", False):
        if len(mensaje.split()) == 1:  # nombre simple
            contexto["nombre"] = mensaje.title()
            contexto["esperando_nombre"] = False
            contexto["iniciado"] = True
            return (f"✨ Encantado de conocerte, <b>{contexto['nombre']}</b> 😊.<br><br>"
                    "¿Qué tipo de carro estás buscando? (ej: SUV, compacto, minivan, pickup, clásico)<br>"
                    "También puedes decir tu <b>presupuesto</b>, <b>color</b>, <b>uso</b> (ciudad, carretera, escolar)..."), contexto
        return ("❌ No reconozco ese nombre. Por favor escribe algo como <b>Carlos</b>."), contexto

    # 3) Color
    color = detectar_color(mensaje)
    if color:
        contexto["color"] = color
        return f"🎨 Anotado, prefieres un auto de color <b>{color}</b>. ¿Quieres que te muestre modelos según categoría o presupuesto?", contexto

    # 4) Categoría
    categoria = detectar_categoria(mensaje)
    if categoria:
        contexto["ultima_categoria"] = categoria
        modelos = buscar_modelos_por_categoria(categoria)
        return (f"{nombre}, te recomiendo estos modelos <b>{categoria}</b>:<br>{formato_modelos_para_texto(modelos)}<br>"
                "👉 ¿Quieres que te diga sobre <b>consumo</b>, <b>mantenimiento</b> o <b>usados</b>?"), contexto

    # 5) Sin intención clara → troleo
    contexto["nonsense_count"] += 1
    if contexto["nonsense_count"] >= 3:
        contexto["nonsense_count"] = 0
        return f"😅 {nombre}, parece que estás jugando... ¿Ya terminaste o seguimos con las recomendaciones?", contexto

    return (f"🤔 {nombre}, no entendí muy bien. Dime si buscas un <b>SUV</b>, <b>compacto</b>, <b>minivan</b>, <b>pickup</b> o incluso un <b>clásico</b>."), contexto
