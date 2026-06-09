from api.peliculas import app
from flask import Response

# Leemos el HTML una sola vez al iniciar
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, 'public', 'index.html')

try:
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        INDEX_HTML = f.read()
except FileNotFoundError:
    INDEX_HTML = "<h1>Error: index.html no encontrado</h1>"

@app.route('/')
def home():
    return Response(INDEX_HTML, mimetype='text/html')

if __name__ == "__main__":
    app.run()