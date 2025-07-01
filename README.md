# ai-image-captioner

## Overview
This project implements an image captioning model using the BLIP architecture. The entire pipeline — from downloading the dataset, preprocessing, training, to inference and submission generation — is implemented in a single Google Colab notebook (`image_captioning.ipynb`). Additionally, a Flask-based web UI allows users to upload images and get captions in real-time using the trained model.

## Steps

1. **Dataset Download & Setup**  
   Use Kaggle API to download the competition dataset directly inside the notebook.  
   Unzip and organize data for processing.

2. **Data Preprocessing**  
   Load the CSV annotations and images.  
   Use Hugging Face’s BLIP processor to prepare images and captions for training.  
   Save the processed dataset as a PyTorch file (`processed_train.pt`).

3. **Model Training**  
   Fine-tune the BLIP model with Hugging Face’s Trainer API inside the notebook.  
   Use training arguments like batch size, learning rate, epochs, etc., as configured in the notebook.  
   Save the best model checkpoint locally and copy it to Google Drive for persistence.

4. **Inference & Submission**  
   Load the saved model checkpoint from Google Drive.  
   Run inference on test images to generate captions.  
   Save the predictions as a submission CSV file.

5. **Web UI for Image Captioning**  
   Flask server hosts a simple web app allowing image upload via HTML form.  
   The backend loads the trained BLIP model and processor.  
   When a user uploads an image, the server processes it and returns the generated caption in real-time.  
   The UI includes frontend code (HTML, CSS, JavaScript) to show results interactively.

## How to Run

### Notebook
- Open `image_captioning.ipynb` in Google Colab.  
- Upload your Kaggle API token (`kaggle.json`) when prompted.  
- Run all notebook cells sequentially — the code handles downloading, preprocessing, training, and inference automatically.  
- Final submission CSV will be saved in the notebook workspace.

### Flask Web UI
- Clone or copy the `app.py` Flask backend and the `templates` and `statics` folders containing HTML/CSS/JS.  
- Ensure Python dependencies are installed (`Flask`, `torch`, `transformers`, `Pillow`).  
- Place the trained model checkpoint folder in the appropriate path.  
- Run the Flask app locally:

```bash
python app.py
```
Open http://localhost:5000 in a browser to upload images and get captions instantly.
![Screenshot 2025-07-02 010830](https://github.com/user-attachments/assets/3174bced-ef6c-47d1-8d41-909ce2a3a631)


### Requirements
- Google Colab (recommended for GPU access during training)
- Python 3.x
- PyTorch
- Transformers (Hugging Face)
- Flask
- pandas
- Pillow

Install Python dependencies with:

```bash
pip install torch transformers flask pandas pillow
