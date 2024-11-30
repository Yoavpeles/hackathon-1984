from flask import Flask, request, jsonify
from flask_cors import CORS
from steganographyBackEnd import embed_message, decode_message

app = Flask(__name__)
CORS(app)

@app.route('/encode', methods=['POST'])
def encode():
    try:
        data = request.form
        image = request.files['image']
        message = data['message']
        output_path = data['output_path']

        image.save('input_image.png')  # Save uploaded image
        embed_message('input_image.png', message, output_path)
        return jsonify({"status": "success", "output_path": output_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/decode', methods=['POST'])
def decode():
    try:
        image = request.files['image']
        image.save('encoded_image.png')  # Save uploaded image
        message = decode_message('encoded_image.png')
        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
