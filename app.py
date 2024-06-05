import datetime
import json
import os

from flask import Flask, jsonify, abort, Blueprint

# Directorio que contiene los archivos JSON
DIRECTORIO_DATOS = 'data/'

# Fecha actual
ANIO = datetime.datetime.now().year
MES = datetime.datetime.now().month
DIA = datetime.datetime.now().day

app = Flask(__name__)

feriados_blueprint = Blueprint('feriados', __name__, url_prefix='/v1/feriados')
feriados_anio_en_curso_blueprint = Blueprint('actual', __name__, url_prefix='/v1/feriados/actual')

# Ruta principal
@app.route("/")
def main_page():
    return "<center><p><body><h2>API de Feriados Nacionales de la República Argentina</h2></p></center>"

# Ruta para obtener la lista de los años disponibles
@feriados_blueprint.route('/lista', methods=['GET'])
def obtener_datos_disponibles():

    # Listar archivos existentes
    archivos = os.listdir(DIRECTORIO_DATOS)
    anios = [int(archivo.split('.')[0].split('_')[2]) for archivo in archivos if archivo.endswith('.json')]

    # Ordenar de mayor a menor
    anios.sort(reverse=True)

    # Retornar json
    return jsonify({"anios": anios})

# Ruta para obtener todos los feriados nacionales de un año especifico
@feriados_blueprint.route('/<int:anio>', methods=['GET'])
def obtener_datos_anio(anio):
    nombre_archivo = rf'feriados_nacionales_{anio}.json'
    ruta_archivo = os.path.join(DIRECTORIO_DATOS, nombre_archivo)

    try:
        with open(ruta_archivo, "r") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return jsonify({"mensaje": "Archivo no encontrado"}), 404

    return jsonify(datos)

# Ruta para obtener las fechas de feriados nacionales por nombre ingresado
@feriados_anio_en_curso_blueprint.route('/<string:query>', methods=['GET'])
def obtener_datos_consulta(query):

    nombre_archivo = rf'feriados_nacionales_{ANIO}.json'
    ruta_archivo = os.path.join(DIRECTORIO_DATOS, nombre_archivo)

    try:
        with open(ruta_archivo, "r") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return jsonify({"mensaje": "Archivo no encontrado"}), 404
    
    datos = [item for item in datos if query.lower() in item['label'].lower()]

    return jsonify(datos)

# Ruta para obtener todos los feriados nacionales de un mes especifico del corriente año
@feriados_anio_en_curso_blueprint.route('/<int:mes>', methods=['GET'])
def obtener_datos_mes(mes):

    if mes < 1 or mes > 12:
        return jsonify({"mensaje": "Mes inválido"}), 400
    
    nombre_archivo = rf'feriados_nacionales_{ANIO}.json'
    ruta_archivo = os.path.join(DIRECTORIO_DATOS, nombre_archivo)
    
    try:
        with open(ruta_archivo, "r") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return jsonify({"mensaje": "Archivo no encontrado"}), 404

    result = []

    for feriado in datos:
        feriado_date = datetime.datetime.strptime(feriado['date'], '%d/%m/%Y')

        if feriado_date.month == mes:
            result.append(feriado)

    if len(result) > 0:
        return jsonify(result)
    else:
        return jsonify({"mensaje": "No hay feriados en este mes"}), 404

# Ruta para obtener el feriado nacional más próximo
@feriados_anio_en_curso_blueprint.route('/proximo', methods=['GET'])
def feriado_proximo():
    nombre_archivo = rf'feriados_nacionales_{ANIO}.json'
    ruta_archivo = os.path.join(DIRECTORIO_DATOS, nombre_archivo)

    try:
        with open(ruta_archivo, "r") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return jsonify({"mensaje": "Archivo no encontrado"}), 404

    for feriado in datos:
        feriado_date = datetime.datetime.strptime(feriado['date'], '%d/%m/%Y')

        if feriado_date.month >= MES and feriado_date.day > DIA:
            return jsonify(feriado)

    return jsonify({"mensaje": "No hay feriados próximos en este año"}), 404

# Bloquear rutas inexistentes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    abort(404, 'Not Found: Invalid URL')

app.register_blueprint(feriados_blueprint)
app.register_blueprint(feriados_anio_en_curso_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
