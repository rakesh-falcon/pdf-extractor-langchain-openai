from fastapi import APIRouter
from mongodb.schemas.loss_run_schema import LossRunIn, LossRunOut
from mongodb.services.loss_run_service import LossRunService

router = APIRouter(prefix="/lossruns", tags=["LossRuns"])

@router.post("/", response_model=LossRunOut)
async def create_loss_run(loss_run: LossRunIn):
    return await LossRunService.create_loss_run(loss_run)

@router.get("/", response_model=list[LossRunOut])
async def get_all_loss_runs():
    return await LossRunService.get_all_loss_runs()