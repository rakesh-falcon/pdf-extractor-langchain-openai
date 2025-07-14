from utils.ocr import extract_text_with_ocr
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schemas.mvr import MVRDriverList
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from collections import Counter
import json, os, re
from datetime import datetime
import fitz
def load_prompt():
    with open("prompts/mvr_prompt.txt", "r") as f:
        return f.read()


def extract_json(text: str) -> list | dict:
    cleaned = text.strip()

    # Try extracting JSON array
    try:
        match = re.search(r"\[\s*{.*}\s*]", cleaned, re.DOTALL)
        if match:
            json_str = match.group()

            # Optional: Fix common formatting issues
            json_str = json_str.replace('}\n{', '},\n{')  # missing comma between objects
            return json.loads(json_str)

    except json.JSONDecodeError as e:
        return {
            "error": "JSON decode failed",
            "raw_response": json_str if 'json_str' in locals() else cleaned[:1000],
            "exception": str(e)
        }

    return {
        "error": "No JSON array found",
        "raw_response": cleaned[:1000]
    }

def get_page_count(file_path: str) -> int:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return len(fitz.open(file_path))
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        return 1
    else:
        return 0
    
async def extract_mvr(files):
    results = []
    prompt_template = ChatPromptTemplate.from_template(load_prompt())
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    for file in files:
        content = await file.read()
        path = f"temp_{file.filename}"
        with open(path, "wb") as f:
            f.write(content)

        text = extract_text_with_ocr(path)
        page_count = get_page_count(path)
        os.remove(path)

        # LLM inference
        response = prompt_template | llm
        raw_output = response.invoke({"text": text}).content

        # Parse JSON list
        parsed = extract_json(raw_output)

        try:
            validated = MVRDriverList.model_validate(parsed).root
            structured = [driver.model_dump() for driver in validated]
        except Exception as e:
            structured = {
                "error": "Schema validation failed",
                "raw_output": parsed,
                "exception": str(e)
            }

        results.append({
            "file_name": file.filename,
            "data": structured,
            "page_count": page_count
        })

    # response_content = add_metadata_per_file({"results": results})
    # return jsonable_encoder(response_content)
    # return response_content
    response_content = add_metadata_per_file({"results": results})
    return jsonable_encoder(response_content)


# def add_metadata_per_file(response: dict) -> dict:
#     for file_info in response.get("results", []):
#         data = file_info.get("data", [])
#         file_info["metadata"] = {
#             "total_drivers": len(data),
#             "extraction_date": datetime.today().strftime("%Y-%m-%d")
#         }
#     return response



def add_metadata_per_file(response: dict) -> dict:
    total_drivers = 0
    total_files = 0
    total_pages = 0
    for file_info in response.get("results", []):
        data = file_info.get("data", [])
        driver_count = len(data) if isinstance(data, list) else 0
        pages = file_info.get("page_count", 0)
        
        file_info["metadata"] = {
            "total_drivers": driver_count,
            "total_pages": pages,
            "extraction_date": datetime.today().strftime("%Y-%m-%d")
        }
        file_info.pop("page_count", None)
        total_drivers += driver_count
        total_files += 1
        total_pages += pages

    response["global_metadata"] = {
        "total_files_processed": total_files,
        "total_drivers_extracted": total_drivers,
        "total_pages": total_pages,
        "extraction_date": datetime.today().strftime("%Y-%m-%d"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    return response
