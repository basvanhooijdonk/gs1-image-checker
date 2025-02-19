import streamlit as st
import cv2
import numpy as np
import requests
import pytesseract
from PIL import Image

# Instellingen voor OCR
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Pas aan als nodig

def download_image(url):
    """Download afbeelding via URL."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return Image.open(response.raw)
    except:
        return None

def check_resolution(image):
    """Controleert of de afbeelding 3000x3000 px is."""
    width, height = image.size
    return width >= 3000 and height >= 3000

def analyze_image(image):
    """Voert de GS1-analyse uit."""
    results = {
        "Resolutie": check_resolution(image),
        "Achtergrond": "Wit" if np.mean(np.array(image)[:10, :10]) > 250 else "Niet wit",
    }
    return results

st.title("📷 GS1 Image Checker")

option = st.radio("Upload methode:", ("URL", "Bestand uploaden"))

if option == "URL":
    url = st.text_input("Voer afbeelding-URL in:")
    if st.button("Analyseren"):
        image = download_image(url)
        if image:
            st.image(image)
            results = analyze_image(image)
            st.json(results)

elif option == "Bestand uploaden":
    uploaded_file = st.file_uploader("Upload een afbeelding", type=["jpg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image)
        results = analyze_image(image)
        st.json(results)
