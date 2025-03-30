from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPTokenAuth
from config import Config


# Initialize extensions without app
ma = Marshmallow()
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address, default_limits=["3 per day"])
auth = HTTPTokenAuth(scheme='Bearer')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with app
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    from routes import init_routes
    # Import and register routes
    init_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)