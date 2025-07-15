from fastapi import FastAPI
from routers import mvr, lossrun

from mongodb.db.init import init_db
from mongodb.api.driver_routes import router as driver_router
from mongodb.api.loss_run_routes import router as loss_run_router

from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="PDF Data Extractor")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(mvr.router, prefix="/api", tags=["MVR"])
app.include_router(mvr.router,prefix="/api", tags=["MVR CONF"])       
# app.include_router(lossrun.router, prefix="/extract/lossrun", tags=["Loss Run"])

app.include_router(driver_router)
app.include_router(loss_run_router)

@app.on_event("startup")
async def on_startup():
    await init_db()