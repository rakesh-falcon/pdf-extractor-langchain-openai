
import fitz
import os
from datetime import datetime
import json, re

def load_prompt():
    with open("prompts/mvr_prompt.txt", "r") as f:
        return f.read()

def load_conf_prompt():
    with open("prompts/mvr_conf_prompt.txt", "r") as f:
        return f.read()

def get_page_count(file_path: str) -> int:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return len(fitz.open(file_path))
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        return 1
    else:
        return 0
    
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
    