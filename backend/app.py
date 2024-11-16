from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import torch
from services.upscaler_service import UpscalerService
from utils.image_utils import save_image, load_image, allowed_file
from config import Config
import traceback

app = Flask(__name__)
# Allow configurable CORS for different environments
CORS(app, resources={r"/api/*": {"origins": os.getenv('ALLOWED_ORIGINS', 'http://localhost:3001').split(',')}})
app.config.from_object(Config)

# Initialize upscaler service with device configuration
upscaler_service = UpscalerService(device=os.getenv('DEVICE', 'cuda' if torch.cuda.is_available() else 'cpu'))

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'gpu_available': torch.cuda.is_available(),
        'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    })

@app.route('/api/upscale', methods=['POST'])
def upscale_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        try:
            # Create directories if they don't exist
            os.makedirs('uploads', exist_ok=True)
            os.makedirs('results', exist_ok=True)

            # Save uploaded image
            input_path = save_image(file, 'uploads')
            prompt = request.form.get('prompt', '')

            # Process image
            output_path = upscaler_service.upscale_image(input_path, prompt)
            
            # Return the processed image
            return send_file(output_path, mimetype='image/png')

        except Exception as e:
            print("Error processing image:", str(e))
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        print("Error in request:", str(e))
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    app.run(debug=True, port=8000, host='0.0.0.0')
