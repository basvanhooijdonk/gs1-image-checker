import streamlit as st
import cv2
import numpy as np
import requests
import pytesseract
from PIL import Image
import io

# Instellingen voor OCR (optioneel, afhankelijk van de vereisten)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Pas aan als nodig

# Functie om een afbeelding van een URL te downloaden
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
        st.error(f"Fout bij downloaden afbeelding: {e}")
        return None

# Functie om te controleren of de afbeelding een minimale resolutie heeft
def check_resolution(image):
    """Controleert of de afbeelding minimaal 3000x3000 px is."""
    width, height = image.size
    return width >= 3000 and height >= 3000

# Functie om de achtergrondkleur van de afbeelding te controleren
def check_background_color(image):
    """Controleer of de achtergrondkleur van de afbeelding wit is."""
    image_np = np.array(image)
    # We nemen het gemiddelde van een groter deel van de afbeelding
    avg_color = np.mean(image_np[:50, :50], axis=(0, 1))
    return "Wit" if np.all(avg_color > 240) else "Niet wit"

# Functie om OCR toe te passen op de afbeelding
def extract_text_from_image(image):
    """Haalt tekst uit de afbeelding met behulp van OCR (Tesseract)."""
    text = pytesseract.image_to_string(image)
    return text

# Functie om de GS1-analyse uit te voeren
def analyze_image(image):
    """Voert een basale GS1-analyse uit (resolutie en achtergrondkleur)."""
    results = {
        "Resolutie (minimaal 3000x3000 px)": check_resolution(image),
        "Achtergrondkleur": check_background_color(image),
    }

    # Voeg OCR-resultaten toe als tekst aanwezig is
    text = extract_text_from_image(image)
    if text.strip():
        results["OCR-tekst"] = text.strip()

    return results

# Streamlit interface
st.title("📷 GS1 Image Checker")

option = st.radio("Kies uploadmethode:", ("URL", "Bestand uploaden"))

if option == "URL":
    url = st.text_input("Voer afbeelding-URL in:")
    if st.button("Analyseren") and url:
        image = download_image(url)
        if image:
            st.image(image, caption="Afbeelding geladen van URL", use_column_width=True)
            results = analyze_image(image)
            st.json(results)

elif option == "Bestand uploaden":
    uploaded_file = st.file_uploader("Upload een afbeelding", type=["jpg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Afbeelding geüpload", use_column_width=True)
        results = analyze_image(image)
        st.json(results)

