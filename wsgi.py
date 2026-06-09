import os
from api.peliculas import app
from flask import send_from_directory

# Obtenemos la carpeta base donde está wsgi.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    # Buscamos index.html en la carpeta 'public' que está al lado de wsgi.py
    public_folder = os.path.join(BASE_DIR, 'public')
    return send_from_directory(public_folder, 'index.html')

if __name__ == "__main__":
    app.run()