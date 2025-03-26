# api.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Database connection settings
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Create a SQLAlchemy instance
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db = SQLAlchemy(app)

# Define a simple model for the API
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    # Add other columns as needed

# Create the database tables
db.create_all()

# API endpoint to retrieve all jobs
@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([job.to_dict() for job in jobs])

# API endpoint to create a new job
@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    new_job = Job(title=data['title'], company=data['company'])
    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)