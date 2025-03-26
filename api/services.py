from flask import request
from api.models import Job
from api.schemas import JobSchema

job_schema = JobSchema()

def get_jobs():
    jobs = Job.query.all()
    return job_schema.dump(jobs, many=True)

def create_job():
    data = request.get_json()
    new_job = Job(title=data['title'], company=data['company'])
    db.session.add(new_job)
    db.session.commit()
    return job_schema.dump(new_job)