
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\RakeshRanjan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_text_with_ocr(file_path: str) -> str:
    full_text = ""

    try:
        doc = fitz.open(file_path)

        for page in doc:
            text = page.get_text()
            if text.strip():
                full_text += text
            else:
                #  Render the page to an image and OCR it
                pix = page.get_pixmap(dpi=300)  # Optional: increase dpi for better OCR
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                full_text += pytesseract.image_to_string(img, config="--psm 6")

    except Exception as e:
        print(f"[OCR ERROR] {file_path}: {e}")
        return ""

    return full_text.strip()
