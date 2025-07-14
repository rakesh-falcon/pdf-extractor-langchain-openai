from fastapi import FastAPI
from routers import mvr, lossrun
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="PDF Data Extractor")

app.include_router(mvr.router, prefix="/api", tags=["MVR"])
# app.include_router(lossrun.router, prefix="/extract/lossrun", tags=["Loss Run"])
