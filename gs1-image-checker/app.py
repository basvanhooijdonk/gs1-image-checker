import streamlit as st
import cv2
import numpy as np
import requests
import pytesseract
from PIL import Image

# Instellingen voor OCR
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Pas aan als nodig

import requests
from PIL import Image
import io

def download_image(url):
    """Download afbeelding van een URL en converteer naar een PIL-image."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()

        # ✅ Controleer de content-type header
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            raise ValueError(f"URL retourneert geen afbeelding, maar {content_type}")

        img = Image.open(io.BytesIO(response.content))
        return img
    except Exception as e:
        print(f"Fout bij downloaden afbeelding: {e}")
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
