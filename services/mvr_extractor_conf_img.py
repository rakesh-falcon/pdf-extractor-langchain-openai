from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from utils.ocr_conf import extract_text_with_ocr_conf_img
from schemas.mvr_conf import MVRDriverConfList
import os
from utils.visualize import  draw_low_conf_boxes
from utils.mvr_utils import extract_json, load_conf_prompt, get_page_count, add_metadata_per_file
from fastapi.encoders import jsonable_encoder
async def extract_mvr_conf(files):
    results = []
    prompt_template = ChatPromptTemplate.from_template(load_conf_prompt())
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    for file in files:
        try:
            content = await file.read()
            path = f"temp_{file.filename}"
            with open(path, "wb") as f:
                f.write(content)

           
            text, ocr_boxes, image = extract_text_with_ocr_conf_img(path)
            page_count = get_page_count(path)

            # Run LLM
            response_chain = prompt_template | llm
            raw_output = response_chain.invoke({"text": text}).content

            # Parse LLM output
            parsed = extract_json(raw_output)

            try:
                validated = MVRDriverConfList.model_validate(parsed).root
                if isinstance(validated, list):
                    structured = [driver.model_dump() for driver in validated]
                else:
                    raise ValueError("Expected a list of driver objects, got single object or invalid format.")
            except Exception as e:
                structured = {
                    "error": "Schema validation failed",
                    "raw_output": parsed,
                    "exception": str(e)
                }
                annotated_blob_url = None
                results.append({
                    "file_name": file.filename,
                    "data": structured,
                    "page_count": page_count,
                    "blob_url": annotated_blob_url
                })
                os.remove(path)
                continue  # skip low-conf logic if schema failed

            # Identify low-confidence fields
            low_conf_values = []

            for driver in structured:
                for field_name, field_data in driver.items():
                    if isinstance(field_data, dict):
                        if field_data.get("conf", 1.0) < 0.9 and field_data.get("value"):
                            val = str(field_data["value"]).strip()
                            if val:
                                low_conf_values.append(val.lower())
            
                    elif isinstance(field_data, list):  # violations
                        for v in field_data:
                            for v_field, v_data in v.items():
                                if isinstance(v_data, dict) and v_data.get("conf", 1.0) < 0.9 and v_data.get("value"):
                                    val = str(v_data["value"]).strip()
                                    if val:
                                        low_conf_values.append(val.lower())
            print(f"OCR boxes extracted: {len(low_conf_values)}")
            print(f"OCR boxes extracted array: {len(ocr_boxes)}")
            # Match values to OCR boxes
            low_conf_boxes = []
            for ocr in ocr_boxes:
                if ocr["word"].lower() in low_conf_values:
                    low_conf_boxes.append(ocr)
            
            # Now draw only those matched
            
            annotated_blob_url = draw_low_conf_boxes(image, low_conf_boxes)

        except Exception as e:
            structured = {
                "error": "Unhandled exception",
                "exception": str(e)
            }
            annotated_blob_url = None

        finally:
            if os.path.exists(path):
                os.remove(path)

        results.append({
            "file_name": file.filename,
            "data": structured,
            "page_count": page_count,
            "blob_url": annotated_blob_url
        })

    response_content = add_metadata_per_file({"results": results})
    return jsonable_encoder(response_content)