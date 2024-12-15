from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import os

# Configuración de Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

app = Flask(__name__)
CORS(app)  # Permitir solicitudes CORS

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear carpeta si no existe

@app.route('/upload', methods=['POST'])
def upload_image():
    try:

        # Verificar si hay archivo en la solicitud
        if 'image' not in request.files:
            return jsonify({"error": "No se envió ninguna imagen"}), 400
        
        file = request.files['image']

        # Guardar temporalmente la imagen
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # Procesar la imagen con Tesseract-OCR
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='spa', config='--psm 6')

        print("aaa",text,image)

        # Eliminar la imagen después del procesamiento
        os.remove(image_path)

        # Retornar el texto extraído
        return jsonify({"text": text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
