from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)

uri = os.environ.get('MONGO_URI') or "mongodb+srv://user_peliculas:PeliProyecto2026!@proyectofinalpeliculas.ib1aupa.mongodb.net/?appName=ProyectoFinalPeliculas"

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['CatalogoPeliculas']
    coleccion = db['peliculas']
except Exception as e:
    print(f"Error de conexión: {e}")

@app.route('/api/insertar', methods=['POST'])
def insertar():
    data = request.json
    try:
        pelicula = {
            "titulo": data['titulo'],
            "genero": data['genero'],
            "anio": int(data['anio']),
            "valoracion": float(data['valoracion'])
        }
        coleccion.insert_one(pelicula)
        return jsonify({"mensaje": "Película guardada con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/buscar_genero', methods=['GET'])
def buscar_genero():
    genero = request.args.get('genero')
    resultados = list(coleccion.find({"genero": {"$regex": genero, "$options": "i"}}))
    # Convertimos los ObjectId a string para que JSON los entienda
    for r in resultados:
        r['_id'] = str(r['_id'])
    return jsonify(resultados)

@app.route('/api/excelentes', methods=['GET'])
def buscar_excelentes():
    resultados = list(coleccion.find({"valoracion": {"$gte": 9}}))
    for r in resultados:
        r['_id'] = str(r['_id'])
    return jsonify(resultados)

@app.route('/api/actualizar', methods=['PUT'])
def actualizar():
    data = request.json
    resultado = coleccion.update_one(
        {"titulo": {"$regex": f"^{data['titulo']}$", "$options": "i"}},
        {"$set": {"valoracion": float(data['valoracion'])}}
    )
    if resultado.modified_count > 0:
        return jsonify({"mensaje": "Actualizado"}), 200
    return jsonify({"mensaje": "No encontrado"}), 404

@app.route('/api/eliminar', methods=['DELETE'])
def eliminar():
    data = request.json
    resultado = coleccion.delete_one({"titulo": {"$regex": f"^{data['titulo']}$", "$options": "i"}})
    if resultado.deleted_count > 0:
        return jsonify({"mensaje": "Eliminado"}), 200
    return jsonify({"mensaje": "No encontrado"}), 404

@app.route('/api/generos', methods=['GET'])
def obtener_generos():
    # Obtiene todos los géneros únicos de la base de datos
    generos = coleccion.distinct('genero')
    # Los ordena alfabéticamente para que se vean mejor en el menú
    generos.sort()
    return jsonify(generos)

if __name__ == '__main__':
    app.run(debug=True)