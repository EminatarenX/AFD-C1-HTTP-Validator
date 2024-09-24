from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import csv
import io
from docx import Document
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
CORS(app)

def afd(cadena):
    # Dividir la cadena en líneas para procesar solicitud HTTP multi-línea
    lineas = cadena.splitlines()

    if len(lineas) < 1:
        return False, ""

    # La primera línea debe contener: <Método> <URL> <Versión HTTP>
    primera_linea = lineas[0].split(" ")
    metodos = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
    versiones = ["HTTP/1.0", "HTTP/1.1", "HTTP/2"]

    if len(primera_linea) != 3:
        return False, ""

    metodo, url, version = primera_linea

    # Validar el método
    if metodo not in metodos:
        return False, ""

    # Validar la URL
    if not url.startswith("/") or " " in url:
        return False, ""

    # Validar la versión HTTP
    if version not in versiones:
        return False, ""

    # Validación opcional de encabezados
    for linea in lineas[1:]:
        if ": " not in linea and linea.strip() != "":
            return False, ""  # Si no tiene el formato clave: valor

    # Clasificar recurso
    if url.startswith("/api/"):
        categoria = "API"
    elif any(url.endswith(ext) for ext in [".html", ".css", ".jpg", ".png", ".js"]):
        categoria = "Recurso Estático"
    elif any(url.endswith(ext) for ext in [".php", ".asp", ".jsp"]):
        categoria = "Recurso Dinámico"
    else:
        categoria = "Otro"

    return True, categoria

@app.route('/')
def home():
    return "¡Bienvenido a la API del autómata HTTP-ReqAnalyzer!"

# Ruta para validar cadenas HTTP (POST)
@app.route('/validar', methods=['POST'])
def validar_cadena():
    data = request.get_json()
    cadena = data.get('cadena', '')
    
    if not cadena:
        return jsonify({'error': 'No se proporcionó ninguna cadena para validar.'}), 400
    
    resultado, categoria = afd(cadena)
    
    if resultado:
        return jsonify({
            'cadena': cadena,
            'aceptada': True,
            'categoria': categoria
        }), 200
    else:
        return jsonify({
            'cadena': cadena,
            'aceptada': False,
            'categoria': 'No aceptada'
        }), 200

# Ruta para obtener todas las cadenas aceptadas o no aceptadas
@app.route('/cadenas', methods=['POST'])
def analizar_cadenas():
    data = request.get_json()
    cadenas = data.get('cadenas', [])
    
    if not cadenas:
        return jsonify({'error': 'No se proporcionaron cadenas para analizar.'}), 400
    
    resultados = []
    for cadena in cadenas:
        resultado, categoria = afd(cadena)
        resultados.append({
            'cadena': cadena,
            'aceptada': resultado,
            'categoria': categoria if resultado else "No aceptada"
        })
    
    return jsonify(resultados), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = file.filename
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension not in ['csv', 'docx', 'html']:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        content = file.read()
        cadenas = []
        
        if file_extension == 'csv':
            csv_content = content.decode('utf-8').splitlines()
            csv_reader = csv.reader(csv_content)
            cadenas = [row[0] for row in csv_reader if row]
        elif file_extension == 'docx':
            doc = Document(io.BytesIO(content))
            cadenas = [para.text for para in doc.paragraphs if para.text.strip()]
        elif file_extension == 'html':
            soup = BeautifulSoup(content, 'html.parser')
            cadenas = [line.strip() for line in soup.stripped_strings if line.strip()]
        
        results = []
        for cadena in cadenas:
            resultado, categoria = afd(cadena)
            results.append({
                'cadena': cadena,
                'aceptada': resultado,
                'categoria': categoria if resultado else "No aceptada"
            })
        
        df = pd.DataFrame(results)
        report_buffer = io.BytesIO()
        df.to_csv(report_buffer, index=False)
        report_buffer.seek(0)
        
        return send_file(
            report_buffer,
            as_attachment=True,
            download_name='report.csv',
            mimetype='text/csv'
        )

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {
        'id': data['id'],
        'name': data['name']
    }
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    updated_item = {
        'id': item_id,
        'name': data['name']
    }
    return jsonify(updated_item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    return jsonify({'message': f'Item {item_id} eliminado'}), 204

if __name__ == '__main__':
    app.run(debug=True)
