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
        
        /* HEADER CON LOGO */
        .header-container { display: flex; align-items: center; gap: 15px; margin-bottom: 30px; padding-left: 10px; }
        .logo-img { height: 60px; width: auto; filter: drop-shadow(0 0 8px rgba(229, 9, 20, 0.3)); transition: transform 0.3s ease; }
        .logo-img:hover { transform: scale(1.05) rotate(-2deg); }
        .site-title { font-size: 2.2rem; color: var(--red); text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid var(--red); padding-bottom: 5px; margin: 0; }
        
        .card { background: var(--card); padding: 25px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); border-left: 4px solid var(--red); }
        h3 { color: var(--red); margin-top: 0; text-transform: uppercase; font-size: 1.1rem; }
        
        input, select { width: 100%; padding: 12px; margin: 8px 0; background: #333; border: 1px solid #444; color: white; border-radius: 4px; box-sizing: border-box; font-size: 1rem; }
        input:focus, select:focus { outline: none; border-color: var(--red); }
        
        button { width: 100%; padding: 12px; margin-top: 10px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; text-transform: uppercase; transition: 0.3s; }
        .btn-primary { background: var(--red); color: white; }
        .btn-primary:hover { background: #f40612; box-shadow: 0 0 10px rgba(229,9,20,0.5); }
        .btn-gold { background: transparent; border: 2px solid var(--gold); color: var(--gold); margin-top: 15px; }
        .btn-gold:hover { background: var(--gold); color: black; }
        .btn-admin { background: transparent; border: 2px solid #fff; color: #fff; margin-top: 10px; }
        .btn-admin:hover { background: #fff; color: black; }
        
        .grid-search { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
        .grid-search input { margin-top: 5px; }
        
        #resultado { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }
        .peli-item { background: #2a2a2a; padding: 15px; border-radius: 8px; border-top: 3px solid var(--gold); animation: fadeIn 0.4s ease; }
        .peli-title { font-size: 1.2rem; font-weight: bold; display: block; margin-bottom: 5px; }
        .peli-meta { color: #b3b3b3; font-size: 0.9rem; }
        .peli-rating { color: var(--gold); font-weight: bold; }
        
        #adminPanel { border-left-color: #fff !important; }
        #adminPanel h3 { color: #fff !important; }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @media (max-width: 600px) { 
            .grid-search { grid-template-columns: 1fr; } 
            .header-container { justify-content: center; padding-left: 0; }
            .site-title { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <!-- HEADER CON LOGO INTEGRADO -->
    <div class="header-container">
        <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBmaWxsPSJub25lIj48cmVjdCB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgZmlsbD0iIzE0MTQxNCIvPjxwYXRoIGQ9Ik0xMDAgMTUwSDQxMlYzNTBIMTAwVjE1MFoiIGZpbGw9IiNFNTA5MTQiLz48cGF0aCBkPSJNMTUwIDEwMEgzNjJMMzEyIDIwMEgxMDBMMTUwIDEwMFoiIGZpbGw9IiNFNTA5MTQiLz48cmVjdCB4PSIxNTAiIHk9IjE4MCIgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSJ3aGl0ZSIvPjxyZWN0IHg9IjIzMCIgeT0iMTgwIiB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIGZpbGw9IndoaXRlIi8+PHJlY3QgeD0iMzEwIiB5PSIxODAiIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCIgZmlsbD0id2hpdGUiLz48cmVjdCB4PSIxNTAiIHk9IjI2MCIgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSJ3aGl0ZSIvPjxyZWN0IHg9IjIzMCIgeT0iMjYwIiB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIGZpbGw9IndoaXRlIi8+PHJlY3QgeD0iMzEwIiB5PSIyNjAiIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCIgZmlsbD0id2hpdGUiLz48cGF0aCBkPSJNMzUwIDIwMEw0MjAgMjU2TDM1MCAzMTJWMjAwWiIgZmlsbD0id2hpdGUiLz48dGV4dCB4PSIyNTYiIHk9IjQ1MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjYwIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC13ZWlnaHQ9ImJvbGQiPkNpbmVNb29kPC90ZXh0Pjwvc3ZnPg==" alt="CineMood Logo" class="logo-img">
        <h1 class="site-title">Catálogo NoSQL</h1>
    </div>

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
        
        <input type="text" id="busquedaTitulo" placeholder="Buscar título (ej: 'Scary' encuentra todas las partes)">
        <button class="btn-primary" onclick="buscarPorTitulo()">Buscar por Nombre</button>

        <div class="grid-search">
            <div>
                <label style="color:#aaa; font-size:0.8rem;">RANGO DE VALORACIÓN</label>
                <div style="display:flex; gap:5px;">
                    <input type="number" id="valMin" placeholder="Min (0)" step="0.1">
                    <input type="number" id="valMax" placeholder="Max (10)" step="0.1">
                </div>
                <button onclick="buscarPorRango()" style="background:#333; color:white; margin-top:5px;">Filtrar Rating</button>
            </div>
            <div>
                <label style="color:#aaa; font-size:0.8rem;">AÑO DE ESTRENO</label>
                <input type="number" id="busquedaAnio" placeholder="Ej: 2000">
                <button onclick="buscarPorAnio()" style="background:#333; color:white; margin-top:5px;">Buscar Año</button>
            </div>
        </div>

        <div style="margin-top: 15px;">
            <label style="color:#aaa; font-size:0.8rem;">FILTRAR POR GÉNERO</label>
            <select id="busquedaGenero"><option>Cargando géneros...</option></select>
            <button onclick="buscarPorGenero()" style="background:#333; color:white; margin-top:5px;">Ver por Género</button>
        </div>

        <button class="btn-gold" onclick="buscarExcelentes()">⭐ Ver Obras Maestras (>= 9.0)</button>
        
        <!-- BOTÓN ADMIN -->
        <button class="btn-admin" onclick="activarAdmin()">🔒 Acceso Administrador</button>
    </div>

    <!-- PANEL ADMIN OCULTO -->
    <div id="adminPanel" class="card" style="display:none;">
        <h3>⚙️ Panel de Administración</h3>
        <p style="color:#aaa; font-size:0.9rem;">Selecciona una película para eliminarla permanentemente.</p>
        <select id="adminSelectPeli" onchange="cargarInfoPeli()">
            <option value="">Cargando catálogo...</option>
        </select>
        <div id="adminInfo" style="margin: 15px 0; padding: 10px; background: #141414; border-radius: 4px; display:none;">
            <strong id="admTitulo" style="color: var(--red);"></strong><br>
            <span id="admMeta" style="color: #888; font-size: 0.9rem;"></span>
        </div>
        <button onclick="eliminarDesdeAdmin()" style="background: #d32f2f; color: white; font-weight: bold;">️ ELIMINAR PELÍCULA SELECCIONADA</button>
        <button onclick="cerrarAdmin()" style="background: #333; color: white; margin-top: 10px;">Cerrar Sesión</button>
    </div>

    <div id="resultado"></div>

    <script>
        const API = '/api';
        const ADMIN_PASS = "admin123";

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

        // --- FUNCIONES ADMIN ---
        async function activarAdmin() {
            const pass = prompt("Ingrese contraseña de administrador:");
            if(pass === ADMIN_PASS) {
                document.getElementById('adminPanel').style.display = 'block';
                await cargarCatalogoAdmin();
                alert("✅ Acceso concedido. Modo Administrador activo.");
            } else if(pass !== null) {
                alert("❌ Contraseña incorrecta.");
            }
        }

        async function cargarCatalogoAdmin() {
            try {
                // Usamos la ruta /api/catalogo que trae TODAS las películas
                const res = await fetch(`${API}/catalogo`);
                const pelis = await res.json();
                const sel = document.getElementById('adminSelectPeli');
                sel.innerHTML = '<option value="">-- Selecciona una película --</option>';
                
                if(pelis.length === 0) {
                    sel.innerHTML += '<option value="">No hay películas en la BD</option>';
                    return;
                }
                
                pelis.forEach(p => {
                    sel.innerHTML += `<option value="${p.titulo}">${p.titulo} (${p.anio}) - ${p.valoracion}</option>`;
                });
            } catch(e) { 
                console.error("Error cargando catálogo admin", e); 
                document.getElementById('adminSelectPeli').innerHTML = '<option>Error al cargar</option>';
            }
        }

        function cargarInfoPeli() {
            const titulo = document.getElementById('adminSelectPeli').value;
            const infoDiv = document.getElementById('adminInfo');
            if(!titulo) { infoDiv.style.display = 'none'; return; }
            const options = document.getElementById('adminSelectPeli').options;
            for(let i=0; i<options.length; i++) {
                if(options[i].value === titulo) {
                    document.getElementById('admTitulo').textContent = options[i].text;
                    infoDiv.style.display = 'block';
                    break;
                }
            }
        }

        async function eliminarDesdeAdmin() {
            const titulo = document.getElementById('adminSelectPeli').value;
            if(!titulo) return alert("Selecciona una película primero");
            if(!confirm(`¿Estás seguro de eliminar "${titulo}"? Esta acción no se puede deshacer.`)) return;
            
            const res = await fetch(`${API}/eliminar`, {
                method: 'DELETE',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({titulo: titulo})
            });
            const json = await res.json();
            if(res.ok) {
                alert("✅ Película eliminada correctamente.");
                await cargarCatalogoAdmin();
                document.getElementById('adminInfo').style.display = 'none';
            } else {
                alert(" Error: " + json.mensaje);
            }
        }

        function cerrarAdmin() {
            document.getElementById('adminPanel').style.display = 'none';
            document.getElementById('adminSelectPeli').value = "";
            document.getElementById('adminInfo').style.display = 'none';
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