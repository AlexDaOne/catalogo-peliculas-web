from api.peliculas import app
from flask import send_from_directory

@app.route('/')
def home():
    return send_from_directory('public', 'index.html')

if __name__ == "__main__":
    app.run()