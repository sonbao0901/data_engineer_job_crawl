from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TopcvDataJob(db.Model):
    __tablename__ = 'topcv_data_job'
    __table_args__ = {'schema': 'bronze'}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    logo = db.Column(db.Text)
    url = db.Column(db.Text, unique=True)
    location = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class ItviecDataJob(db.Model):
    __tablename__ = 'itviec_data_job'
    __table_args__ = {'schema': 'bronze'}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    logo = db.Column(db.Text)
    url = db.Column(db.Text, unique=True)
    location = db.Column(db.String(100))
    mode = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    descriptions = db.Column(db.Text)
    requirements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())