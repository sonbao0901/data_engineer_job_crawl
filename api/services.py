from api.models import TopcvDataJob, ItviecDataJob
from api.schemas import topcv_job_schema, itviec_job_schema
from api.app import db

def get_topcv_jobs():
    try:
        jobs = TopcvDataJob.query.all()
        return topcv_job_schema.dump(jobs, many=True)
    except Exception as e:
        raise Exception(f"Failed to fetch TopCV jobs: {str(e)}")

def get_itviec_jobs():
    try:
        jobs = ItviecDataJob.query.all()
        return itviec_job_schema.dump(jobs, many=True)
    except Exception as e:
        raise Exception(f"Failed to fetch ITViec jobs: {str(e)}")