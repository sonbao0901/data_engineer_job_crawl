from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services import get_topcv_jobs, get_itviec_jobs
from schemas import TopcvDataJob, ItviecDataJob
from dependencies import limiter

router = APIRouter()

@router.get("/topcv/jobs", response_model=List[TopcvDataJob])
@limiter.limit("3/day")
async def get_topcv_jobs_endpoint(request: Request, db: Session = Depends(get_db)):
    """
    Get all TopCV jobs
    """
    try:
        jobs = get_topcv_jobs(db)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/itviec/jobs", response_model=List[ItviecDataJob])
@limiter.limit("3/day")
async def get_itviec_jobs_endpoint(request: Request, db: Session = Depends(get_db)):
    """
    Get all ITViec jobs
    """
    try:
        jobs = get_itviec_jobs(db)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))