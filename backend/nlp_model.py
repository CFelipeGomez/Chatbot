import spacy

# -------------------------------------------------------------------
# Cargar el modelo de spaCy en español
# -------------------------------------------------------------------
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    from spacy.cli import download
    download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")


# -------------------------------------------------------------------
# Función: analizar texto (tokenización, lematización, POS tagging)
# -------------------------------------------------------------------
def analizar_texto(texto: str):
    """
    Procesa un texto en español usando spaCy.
    Devuelve una lista de tuplas con:
    - Palabra original
    - Lema
    - Etiqueta gramatical (POS)
    """
    doc = nlp(texto)
    tokens = [(token.text, token.lemma_, token.pos_) for token in doc]
    return tokens


# -------------------------------------------------------------------
# Función: extraer entidades (NER)
# -------------------------------------------------------------------
def extraer_entidades(texto: str):
    """
    Extrae entidades nombradas (NER) del texto.
    Ejemplo: marcas, ubicaciones, fechas, cantidades, etc.
    Devuelve una lista de tuplas con:
    - Entidad
    - Tipo de entidad
    """
    doc = nlp(texto)
    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    return entidades


# -------------------------------------------------------------------
# Función: preprocesar texto para clasificación de intención
# -------------------------------------------------------------------
def limpiar_texto(texto: str):
    """
    Preprocesa el texto para análisis posterior:
    - Convierte a minúsculas
    - Elimina signos de puntuación y espacios innecesarios
    - Retorna una lista de lemas (palabras base)
    """
    doc = nlp(texto.lower())
    lemas = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return lemas
