from api.peliculas import app
from flask import Response

INDEX_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Películas</title>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    :root {
        --bg-color: #141414;
        --card-bg: #1f1f1f;
        --primary: #E50914;
        --accent: #FF9900;
        --text-main: #ffffff;
        --text-sec: #b3b3b3;
        --radius: 8px;
    }

    body {
        font-family: 'Montserrat', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-main);
        margin: 0;
        padding: 20px;
        min-height: 100vh;
    }

    h1 {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 30px;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-bottom: 2px solid var(--primary);
        display: inline-block;
        padding-bottom: 10px;
        width: 100%;
    }

    .card {
        background-color: var(--card-bg);
        padding: 25px;
        border-radius: var(--radius);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 25px;
        border-left: 4px solid var(--primary);
        transition: transform 0.2s ease;
    }

    .card:hover {
        transform: translateY(-3px);
    }

    h3 {
        margin-top: 0;
        color: var(--primary);
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    input {
        background-color: #333;
        border: 1px solid #444;
        color: white;
        padding: 12px;
        margin: 8px 0;
        width: 100%;
        box-sizing: border-box;
        border-radius: 4px;
        font-size: 1rem;
        transition: border-color 0.3s;
    }

    input:focus {
        outline: none;
        border-color: var(--primary);
        background-color: #444;
    }

    button {
        padding: 12px 20px;
        margin: 10px 5px 0 0;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        width: 100%;
    }

    button[onclick="insertar()"], 
    button[onclick="buscarGenero()"] {
        background-color: var(--primary);
        color: white;
    }

    button[onclick="insertar()"]:hover, 
    button[onclick="buscarGenero()"]:hover {
        background-color: #f40612;
        box-shadow: 0 0 10px rgba(229, 9, 20, 0.4);
    }

    button[onclick="buscarExcelentes()"] {
        background-color: transparent;
        border: 2px solid var(--accent);
        color: var(--accent);
    }

    button[onclick="buscarExcelentes()"]:hover {
        background-color: var(--accent);
        color: black;
        box-shadow: 0 0 10px rgba(255, 153, 0, 0.4);
    }

    #resultado {
        margin-top: 30px;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 20px;
    }

    .peli-item {
        background-color: #2a2a2a;
        padding: 15px;
        border-radius: var(--radius);
        border-top: 3px solid var(--accent);
        animation: fadeIn 0.5s ease;
    }

    .peli-item strong {
        display: block;
        font-size: 1.1rem;
        margin-bottom: 5px;
        color: white;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 600px) {
        h1 { font-size: 1.8rem; }
        .card { padding: 15px; }
    }
</style>
</head>
<body>
    <h1>🎬 Catálogo de Películas</h1>

    <div class="card">
        <h3>Insertar Película</h3>
        <input type="text" id="titulo" placeholder="Título">
        <input type="text" id="genero" placeholder="Género">
        <input type="number" id="anio" placeholder="Año">
        <input type="number" id="valoracion" placeholder="Valoración (0-10)" step="0.1">
        <button onclick="insertar()">Guardar Película</button>
    </div>

    <div class="card">
        <h3>Buscar por Género</h3>
        <input type="text" id="busquedaGenero" placeholder="Ej: Acción">
        <button onclick="buscarGenero()">Buscar</button>
        <button onclick="buscarExcelentes()" style="background-color: #ff9900;">Ver Excelentes (>=9)</button>
    </div>

    <div id="resultado"></div>

    <script>
        const API_URL = '/api'; 

        async function insertar() {
            const data = {
                titulo: document.getElementById('titulo').value,
                genero: document.getElementById('genero').value,
                anio: document.getElementById('anio').value,
                valoracion: document.getElementById('valoracion').value
            };
            
            const res = await fetch(`${API_URL}/insertar`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const json = await res.json();
            alert(json.mensaje || json.error);
        }

        async function buscarGenero() {
            const genero = document.getElementById('busquedaGenero').value;
            const res = await fetch(`${API_URL}/buscar_genero?genero=${genero}`);
            const pelis = await res.json();
            mostrarResultados(pelis);
        }

        async function buscarExcelentes() {
            const res = await fetch(`${API_URL}/excelentes`);
            const pelis = await res.json();
            mostrarResultados(pelis);
        }

        function mostrarResultados(pelis) {
            const div = document.getElementById('resultado');
            div.innerHTML = '';
            if(pelis.length === 0) {
                div.innerHTML = '<p>No se encontraron resultados.</p>';
                return;
            }
            pelis.forEach(p => {
                div.innerHTML += `<div class="peli-item"><strong>${p.titulo}</strong> (${p.anio}) - ${p.genero} | ⭐ ${p.valoracion}</div>`;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return Response(INDEX_HTML, mimetype='text/html')

if __name__ == "__main__":
    app.run()