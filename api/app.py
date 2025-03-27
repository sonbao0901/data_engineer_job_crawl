from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
app.config.from_object('api.config.Config')

db = SQLAlchemy(app)
ma = Marshmallow(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3 per day"]
)

auth = HTTPTokenAuth(scheme='Bearer')

from api.models import Job
from api.schemas import JobSchema
from api.services import get_jobs, create_job

@app.route('/jobs', methods=['GET'])
@limiter.limit("3 per day")
@auth.login_required
def get_jobs_endpoint():
    return jsonify(get_jobs())

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
