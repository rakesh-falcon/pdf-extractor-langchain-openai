import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\RakeshRanjan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_text_with_ocr_conf_img(file_path: str) -> tuple[str, list[dict], Image.Image]:
    full_text = ""
    ocr_boxes = []

    try:
        doc = fitz.open(file_path)

        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))

            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

            for i in range(len(data["text"])):
                word = data["text"][i].strip()
                if word:
                    full_text += word + " "
                    bbox = [data["left"][i], data["top"][i], data["width"][i], data["height"][i]]
                    ocr_boxes.append({"word": word.lower(), "bbox": bbox})

    except Exception as e:
        print(f"[OCR ERROR] {file_path}: {e}")
        return "", []
    print(ocr_boxes)
    return full_text.strip(), ocr_boxes, img



# def extract_text_with_ocr(file_path: str) -> tuple[str, list[dict], Image.Image]:
#     full_text = ""
#     ocr_boxes = []

#     try:
#         doc = fitz.open(file_path)

#         for page in doc:
#             pix = page.get_pixmap(dpi=300)
#             img_bytes = pix.tobytes("png")
#             img = Image.open(io.BytesIO(img_bytes))

#             data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

#             for i in range(len(data["text"])):
#                 word = data["text"][i].strip()
#                 if word:
#                     full_text += word + " "
#                     bbox = [data["left"][i], data["top"][i], data["width"][i], data["height"][i]]
#                     ocr_boxes.append({"word": word.lower(), "bbox": bbox})

#     except Exception as e:
#         print(f"[OCR ERROR] {file_path}: {e}")
#         return "", []
#     print(ocr_boxes)
#     return full_text.strip(), ocr_boxes, img