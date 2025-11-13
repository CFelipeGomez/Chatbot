# Chatbot Experto en Autos 🚗

## Descripción del Proyecto

Este proyecto implementa un Chatbot conversacional diseñado para recomendar vehículos. Utiliza un *backend* construido con **Python** y el microframework **Flask** para la API, e incorpora el poder del Procesamiento de Lenguaje Natural (**NLP**) mediante la librería **spaCy** para entender las intenciones y extraer entidades del usuario. El *frontend* es una interfaz de chat simple en **HTML, CSS y JavaScript** que se comunica con la API del backend.

El chatbot es capaz de mantener el contexto de la conversación, detectar preferencias como nombres, colores, y categorías de vehículos, y ofrecer recomendaciones específicas.

## Características Principales

* **Recomendación Conversacional:** Guía al usuario a través de una conversación para refinar la búsqueda del auto ideal.
* **Procesamiento de Lenguaje Natural (NLP):** Utiliza spaCy con el modelo en español (`es_core_news_sm`) para:
    * Tokenización, lematización y etiquetado gramatical (POS tagging).
    * Extracción de entidades nombradas (NER).
    * Limpieza y preprocesamiento de texto para el análisis de intención.
* **Detección de Intenciones:** Puede identificar el nombre del usuario, color preferido, y la categoría de vehículo (ej: SUV, compacto, minivan, pickup, clásico).
* **Interfaz Web:** Interfaz de chat interactiva en el navegador.

## Tecnologías

### Backend
* **Python**
* **Flask** (Framework del servidor web)
* **spaCy** (Procesamiento de Lenguaje Natural)
* **nltk** (Natural Language Toolkit)
* **flask-cors** (Para manejar peticiones entre frontend y backend)

### Frontend
* **HTML5**
* **CSS3**
* **JavaScript** (Realiza peticiones `POST` a la API del backend)

## Estructura del Proyecto
Directory structure:

└── cfelipegomez-chatbot/

    ├── backend/
    
    │   ├── app.py
    
    │   ├── nlp_model.py
    
    │   ├── recommender.py
    
    │   └── requirements.txt
    
    └── frontend/
    
        ├── index.html
        
        ├── script.js
        
        └── styles.css


## Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

### 1. Clonar el Repositorio (o descomprimir)

Si tienes los archivos localmente en la estructura anterior, omite este paso.

### 2. Configurar el Backend (Python/Flask)

1.  **Navega al directorio `backend`**:
    ```bash
    cd backend
    ```

2.  **Crear y activar un entorno virtual** (opcional, pero recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate  # En Windows
    ```

3.  **Instalar las dependencias de Python**:
    ```bash
    pip install -r requirements.txt
    ```
    *Nota: Las dependencias incluyen `Flask`, `spacy`, `nltk`, entre otras.*

4.  **Descargar el modelo de spaCy en español** (Si no se descarga automáticamente en `nlp_model.py`):
    ```bash
    python -m spacy download es_core_news_sm
    ```

5.  **Ejecutar la aplicación Flask**:
    ```bash
    python app.py
    ```
    El servidor se ejecutará por defecto en `http://127.0.0.1:5000` en modo *debug*.

### 3. Ejecutar el Frontend (Web)

1.  **Navega al directorio `frontend`**:
    ```bash
    cd ../frontend
    ```

2.  **Abrir `index.html`** directamente en tu navegador.
    * La lógica de JavaScript está configurada para enviar peticiones al endpoint `http://127.0.0.1:5000/chat`. Asegúrate de que el servidor Flask esté corriendo.

## Uso del Chatbot

1.  Abre el archivo `frontend/index.html` en tu navegador.
2.  Escribe un mensaje en la caja de texto y presiona **Enter** o haz clic en **Enviar**.
3.  El chatbot te guiará pidiéndote información sobre el auto que buscas, como tu nombre, el tipo de vehículo (`SUV`, `compacto`, etc.), o tu presupuesto.

## Endpoints de la API (Backend)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/chat` | Recibe un mensaje del usuario, lo procesa con NLP, lo pasa al motor de recomendación y devuelve una respuesta. |

**Ejemplo de Petición (vía Frontend/JavaScript):**

La función `sendMessage` envía un objeto JSON con el mensaje del usuario:

```json
{
    "message": "Hola, estoy buscando un SUV."
}
