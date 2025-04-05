from sqlalchemy.orm import Session
from models import TopcvDataJob, ItviecDataJob
from schemas import TopcvDataJob as TopcvDataJobSchema, ItviecDataJob as ItviecDataJobSchema
from typing import List

def get_topcv_jobs(db: Session) -> List[TopcvDataJobSchema]:
    """
    Retrieve all TopCV jobs from the database
    """
    try:
        jobs = db.query(TopcvDataJob).all()
        return jobs
    except Exception as e:
        raise Exception(f"Failed to fetch TopCV jobs: {str(e)}")

def get_itviec_jobs(db: Session) -> List[ItviecDataJobSchema]:
    """
    Retrieve all ITViec jobs from the database
    """
    try:
        jobs = db.query(ItviecDataJob).all()
        return jobs
    except Exception as e:
        raise Exception(f"Failed to fetch ITViec jobs: {str(e)}")