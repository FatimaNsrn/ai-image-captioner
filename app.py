import os
from flask import Flask, request, jsonify, render_template
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests

app = Flask(__name__)

# Google Drive file ID of your checkpoint folder archive (e.g., a zipped model folder)
MODEL_DRIVE_FILE_ID = '14XpMmekx6K4Gzfv59FY8yMbCOGj2EgPW'
MODEL_ZIP_NAME = 'best_checkpoint.zip'
MODEL_FOLDER = 'best_checkpoint'

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

def check_and_download_model():
    if not os.path.exists(MODEL_FOLDER):
        print(f"Model folder not found locally. Downloading from Google Drive as {MODEL_ZIP_NAME}...")
        download_file_from_google_drive(MODEL_DRIVE_FILE_ID, MODEL_ZIP_NAME)
        print("Download completed. Extracting...")
        import zipfile
        with zipfile.ZipFile(MODEL_ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall('.')
        print("Extraction complete.")
        os.remove(MODEL_ZIP_NAME)
    else:
        print("Model folder found locally.")

# Check and download model before loading
check_and_download_model()

# Load model and processor
print("Loading BLIP model and processor from local checkpoint...")
processor = BlipProcessor.from_pretrained(MODEL_FOLDER)
model = BlipForConditionalGeneration.from_pretrained(MODEL_FOLDER)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
print("Model loaded!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream).convert('RGB')

    inputs = processor(image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(**inputs)

    caption = processor.decode(outputs[0], skip_special_tokens=True)

    return jsonify({'caption': caption})

if __name__ == '__main__':
    app.run(debug=True)
