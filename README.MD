# PDF Extractor using LangChain, FastAPI & OpenAI 

A modular and scalable system to extract structured JSON data from normal and scanned PDFs like:

-  MVR (Motor Vehicle Reports)
-  Loss Run Reports

Supports multi-file uploads, schema validation, OCR, and LLM-based parsing.

---

1. **Upload a PDF or Image** and receive  `JSON`.

---

##  Tech Stack

- **FastAPI** – API framework  
- **LangChain + OpenAI** – Document understanding  
- **Pydantic** – Schema validation  
- **Tesseract OCR** – Scanned PDF support  
- **Python 3.10+**

---

## Features

- Upload PDF/Image files and extract their content
- Query extracted content using natural language (e.g., "What is the driver's license number?")
- Powered by LangChain, OpenAI, or other LLMs (configurable)
- Session-based context for follow-up questions

---

## Project Structure

**Main folders:**

- `main.py`: FastAPI entry point  
- `routers/`: API route handlers (`mvr.py`, `lossrun.py`)  
- `services/`: Business logic and LLM/OCR integration  
- `schemas/`: Pydantic models for output validation  
- `prompts/`: Custom prompt templates (e.g., `mvr_prompt.txt`)  
- `utils/ocr.py`: OCR utility using Tesseract  
- `.env`: Your OpenAI API key and environment configs  

---

##  Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/rakesh-falcon/pdf-extractor-langchain-openai.git
cd pdf-extractor-langchain-openai
```

### 2. Create Virtual Environment

- python -m venv venv
- source venv/bin/activate      # Windows: venv\Scripts\activate

### 3. Install Dependencies
- pip install -r requirements.txt

### 4. Configure Environment Variables

- Create a .env file in the root directory:

- OPENAI_API_KEY=your_openai_api_key_here

### 5. Run the API

- uvicorn main:app --reload
- Open in browser: http://localhost:8000/docs

---

## API Endpoints

`POST --> /api/mvr`

Accepts multiple .pdf files

Returns structured driver info and violations

`POST --> /api/mvr-conf`

Accepts multiple .pdf files

Returns structured driver info and violations with conf score.

---

## Adding New Document Type

### 1. Add prompt to prompts/
### 2. Create schema in schemas/
### 3. Write logic in services/
### 4. Add route in routers/

---

## Key Dependencies
- fastapi
- langchain
- langchain-openai
- openai
- python-dotenv
- pytesseract
- pymupdf (fitz)
- pillow
- uvicorn

---

## Features
- Normal + scanned PDF support (OCR fallback)
- Multi-file upload
- LLM-based extraction
- Schema-validated JSON
- Easily extendable with prompt-based control

---

## License

This project is licensed under the MIT License.

---

## Support

For issues, bugs, or feature requests, please open an issue on the [GitHub repo](https://github.com/rakesh-falcon/pdf-extractor-langchain-openai.git).


