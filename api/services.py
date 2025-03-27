from flask import request
from api.models import Job
from api.schemas import JobSchema

job_schema = JobSchema()

def get_jobs():
    jobs = Job.query.all()
    return job_schema.dump(jobs, many=True)
