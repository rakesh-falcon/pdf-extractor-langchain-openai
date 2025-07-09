import fitz
from PIL import Image
import pytesseract
import io

def extract_text_with_ocr(file_path: str) -> str:
    doc = fitz.open(file_path)
    full_text = ""

    for page in doc:
        text = page.get_text()
        if text.strip():
            full_text += text
        else:
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            full_text += pytesseract.image_to_string(img)

    return full_text
