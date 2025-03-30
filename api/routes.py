from flask import jsonify
from services import get_topcv_jobs, get_itviec_jobs
from app import limiter, db
from functools import wraps

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return wrapper

def init_routes(app):
    @app.route('/')
    def home():
        return "API is running", 200
    
    @app.route('/topcv/jobs', methods=['GET'])
    @limiter.limit("3 per day")
    @handle_errors
    def get_topcv_jobs_endpoint():
        with app.app_context():  # Ensure database operations have context
            return jsonify(get_topcv_jobs())
    
    @app.route('/itviec/jobs', methods=['GET'])
    @limiter.limit("3 per day")
    @handle_errors
    def get_itviec_jobs_endpoint():
        with app.app_context():  # Ensure database operations have context
            return jsonify(get_itviec_jobs())