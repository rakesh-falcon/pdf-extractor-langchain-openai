from fastapi import APIRouter, UploadFile, File
from services.mvr_extractor import extract_mvr

router = APIRouter()

@router.post("/mvr")
async def extract_mvr_data(files: list[UploadFile] = File(...)):
    return await extract_mvr(files)

