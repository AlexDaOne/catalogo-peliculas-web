from api.peliculas import app
from flask import Response

# --- TODO EL SITIO WEB ESTÁ AQUÍ DENTRO ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CineMood - Catálogo NoSQL</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
        :root { --bg: #141414; --card: #1f1f1f; --red: #E50914; --gold: #FF9900; --txt: #fff; }
        body { font-family: 'Montserrat', sans-serif; background: var(--bg); color: var(--txt); margin: 0; padding: 20px; min-height: 100vh; }
        h1 { text-align: center; color: var(--red); text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid var(--red); padding-bottom: 10px; }
        
        .card { background: var(--card); padding: 25px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); border-left: 4px solid var(--red); }
        h3 { color: var(--red); margin-top: 0; text-transform: uppercase; font-size: 1.1rem; }
        
        input, select { width: 100%; padding: 12px; margin: 8px 0; background: #333; border: 1px solid #444; color: white; border-radius: 4px; box-sizing: border-box; font-size: 1rem; }
        input:focus, select:focus { outline: none; border-color: var(--red); }
        
        button { width: 100%; padding: 12px; margin-top: 10px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; text-transform: uppercase; transition: 0.3s; }
        .btn-primary { background: var(--red); color: white; }
        .btn-primary:hover { background: #f40612; box-shadow: 0 0 10px rgba(229,9,20,0.5); }
        .btn-gold { background: transparent; border: 2px solid var(--gold); color: var(--gold); margin-top: 15px; }
        .btn-gold:hover { background: var(--gold); color: black; }
        
        .grid-search { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
        .grid-search input { margin-top: 5px; }
        
        #resultado { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }
        .peli-item { background: #2a2a2a; padding: 15px; border-radius: 8px; border-top: 3px solid var(--gold); animation: fadeIn 0.4s ease; }
        .peli-title { font-size: 1.2rem; font-weight: bold; display: block; margin-bottom: 5px; }
        .peli-meta { color: #b3b3b3; font-size: 0.9rem; }
        .peli-rating { color: var(--gold); font-weight: bold; }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @media (max-width: 600px) { .grid-search { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <h1>🎬 CineMood Catalog</h1>

    <!-- INSERTAR -->
    <div class="card">
        <h3>Agregar Película</h3>
        <input type="text" id="titulo" placeholder="Título exacto">
        <input type="text" id="generoInput" placeholder="Género (ej: Acción)">
        <input type="number" id="anio" placeholder="Año (ej: 2024)">
        <input type="number" id="valoracion" placeholder="Valoración (0-10)" step="0.1">
        <button class="btn-primary" onclick="insertar()">Guardar en Base de Datos</button>
    </div>

    <!-- BÚSQUEDAS AVANZADAS -->
    <div class="card">
        <h3>🔍 Búsqueda Inteligente</h3>
        
        <!-- Por Título (Principal) -->
        <input type="text" id="busquedaTitulo" placeholder="Buscar título (ej: 'Scary' encuentra todas las partes)">
        <button class="btn-primary" onclick="buscarPorTitulo()">Buscar por Nombre</button>

        <div class="grid-search">
            <!-- Por Valoración -->
            <div>
                <label style="color:#aaa; font-size:0.8rem;">RANGO DE VALORACIÓN</label>
                <div style="display:flex; gap:5px;">
                    <input type="number" id="valMin" placeholder="Min (0)" step="0.1">
                    <input type="number" id="valMax" placeholder="Max (10)" step="0.1">
                </div>
                <button onclick="buscarPorRango()" style="background:#333; color:white; margin-top:5px;">Filtrar Rating</button>
            </div>

            <!-- Por Año -->
            <div>
                <label style="color:#aaa; font-size:0.8rem;">AÑO DE ESTRENO</label>
                <input type="number" id="busquedaAnio" placeholder="Ej: 2000">
                <button onclick="buscarPorAnio()" style="background:#333; color:white; margin-top:5px;">Buscar Año</button>
            </div>
        </div>

        <!-- Por Género (Dinámico) -->
        <div style="margin-top: 15px;">
            <label style="color:#aaa; font-size:0.8rem;">FILTRAR POR GÉNERO</label>
            <select id="busquedaGenero"><option>Cargando géneros...</option></select>
            <button onclick="buscarPorGenero()" style="background:#333; color:white; margin-top:5px;">Ver por Género</button>
        </div>

        <button class="btn-gold" onclick="buscarExcelentes()">⭐ Ver Obras Maestras (>= 9.0)</button>
    </div>

    <div id="resultado"></div>

    <script>
        const API = '/api';

        // Cargar géneros al iniciar
        window.onload = async () => {
            try {
                const res = await fetch(`${API}/generos`);
                const generos = await res.json();
                const sel = document.getElementById('busquedaGenero');
                sel.innerHTML = '<option value="">-- Todos los géneros --</option>';
                generos.forEach(g => {
                    sel.innerHTML += `<option value="${g}">${g}</option>`;
                });
            } catch(e) { console.error("Error cargando géneros", e); }
        };

        // Funciones de búsqueda
        async function buscarPorTitulo() {
            const q = document.getElementById('busquedaTitulo').value;
            if(!q) return alert("Escribe un título");
            const res = await fetch(`${API}/buscar_titulo?q=${encodeURIComponent(q)}`);
            mostrar(await res.json(), `Resultados para "${q}"`);
        }

        async function buscarPorRango() {
            const min = document.getElementById('valMin').value || 0;
            const max = document.getElementById('valMax').value || 10;
            const res = await fetch(`${API}/buscar_rango?min=${min}&max=${max}`);
            mostrar(await res.json(), `Rating entre ${min} y ${max}`);
        }

        async function buscarPorAnio() {
            const anio = document.getElementById('busquedaAnio').value;
            if(!anio) return alert("Ingresa un año");
            const res = await fetch(`${API}/buscar_anio?anio=${anio}`);
            mostrar(await res.json(), `Estrenos de ${anio}`);
        }

        async function buscarPorGenero() {
            const g = document.getElementById('busquedaGenero').value;
            if(!g) return alert("Selecciona un género");
            const res = await fetch(`${API}/buscar_genero?genero=${g}`);
            mostrar(await res.json(), `Género: ${g}`);
        }

        async function buscarExcelentes() {
            const res = await fetch(`${API}/excelentes`);
            mostrar(await res.json(), "⭐ Obras Maestras (>= 9.0)");
        }

        async function insertar() {
            const data = {
                titulo: document.getElementById('titulo').value,
                genero: document.getElementById('generoInput').value,
                anio: document.getElementById('anio').value,
                valoracion: document.getElementById('valoracion').value
            };
            const res = await fetch(`${API}/insertar`, {
                method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)
            });
            const json = await res.json();
            alert(json.mensaje || json.error);
            // Recargar géneros por si acaso se agregó uno nuevo
            window.onload(); 
        }

        function mostrar(pelis, titulo) {
            const div = document.getElementById('resultado');
            div.innerHTML = `<h2 style="color:var(--gold); width:100%;">${titulo}</h2>`;
            if(pelis.length === 0) {
                div.innerHTML += '<p style="color:#888; width:100%;">No se encontraron películas.</p>';
                return;
            }
            pelis.forEach(p => {
                div.innerHTML += `
                <div class="peli-item">
                    <span class="peli-title">${p.titulo}</span>
                    <div class="peli-meta">
                         ${p.anio} | 🎭 ${p.genero}<br>
                        <span class="peli-rating">⭐ ${p.valoracion}/10</span>
                    </div>
                </div>`;
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