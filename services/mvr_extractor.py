from utils.ocr import extract_text_with_ocr
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schemas.mvr import MVRDriverList
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from collections import Counter
import json, os, re

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
            "data": structured
        })

    # response_content = add_metadata_per_file({"results": results})
    # return jsonable_encoder(response_content)
    return results


def add_metadata_per_file(response: dict) -> dict:
    for file_info in response.get("results", []):
        data = file_info.get("data", [])
        file_info["metadata"] = {
            "total_drivers": len(data),
            "extraction_date": datetime.today().strftime("%Y-%m-%d")
        }
    return response

# def add_metadata_per_file(response: dict) -> dict:
#     for file_info in response.get("results", []):
#         data = file_info.get("data", [])

#         violations = []
#         for d in data:
#             v_list = d.get("violations", [])
#             if isinstance(v_list, list):
#                 for v in v_list:
#                     if isinstance(v, dict) and v.get("violation_description"):
#                         violations.append(v["violation_description"])

#         license_statuses = [d.get("license_status") for d in data if d.get("license_status")]
#         license_classes = sorted(set(d.get("lic_class") for d in data if d.get("lic_class")))
#         states = sorted(set(d.get("state_of_driver_record") for d in data if d.get("state_of_driver_record")))

#         file_info["metadata"] = {
#             "file_name": file_info.get("file_name"),
#             "extraction_date": datetime.today().strftime("%Y-%m-%d"),
#             "total_drivers": len(data),
#             "drivers_with_violations": sum(
#                 1 for d in data
#                 if isinstance(d.get("violations", []), list) and d.get("violations")
#             ),
#             "total_violations": len(violations),
#             "license_status_summary": dict(Counter(license_statuses)),
#             "license_classes": license_classes,
#             "states_involved": states,
#             "violations_summary": dict(Counter(violations))
#         }

#     return response
