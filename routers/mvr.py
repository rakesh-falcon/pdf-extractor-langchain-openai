from fastapi import APIRouter, UploadFile, File
from services.mvr_extractor import extract_mvr ,extract_mvr_conf

router = APIRouter()

@router.post("/mvr")
async def extract_mvr_data(files: list[UploadFile] = File(...)):
    return await extract_mvr(files)

@router.post("/mvr-conf")
async def extract_mvr_data_conf(files: list[UploadFile] = File(...)):
    return await extract_mvr_conf(files) 

