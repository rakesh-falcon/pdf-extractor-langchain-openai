from utils.ocr import extract_text_with_ocr
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schemas.mvr import MVRDriverList
from schemas.mvr_conf import MVRDriverConfList
from fastapi.encoders import jsonable_encoder
from utils.mvr_utils import extract_json, load_prompt , load_conf_prompt, get_page_count, add_metadata_per_file
import os
import traceback


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

    response_content = add_metadata_per_file({"results": results})
    return jsonable_encoder(response_content)


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

            text = extract_text_with_ocr(path)
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
                    "exception": str(e),
                    "traceback": traceback.format_exc()
                }
                # annotated_blob_url = None
                results.append({
                    "file_name": file.filename,
                    "data": structured,
                    "page_count": page_count
                })
                os.remove(path)
                continue  # skip low-conf logic if schema failed

        except Exception as e:
            structured = {
                "error": "Unhandled exception",
                "exception": str(e),
                "traceback": traceback.format_exc()
            }

        finally:
            if os.path.exists(path):
                os.remove(path)

        results.append({
            "file_name": file.filename,
            "data": structured,
            "page_count": page_count
        })

    response_content = add_metadata_per_file({"results": results})
    return jsonable_encoder(response_content)
