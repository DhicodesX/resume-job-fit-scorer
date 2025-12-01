# app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# import the single db instance
from extensions import db

# import blueprints
from routes.upload import upload_bp
from routes.job_upload import job_bp
from routes.match import match_bp

# import models so migrations can detect them
from models.resume import Resume

load_dotenv()

def create_app():
    app = Flask(__name__)

    # config
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'resume_scorer.db')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'jwt-secret-string')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))

    # initialize extensions with the app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    # ensure folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # register blueprints
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(job_bp, url_prefix='/api/job')
    app.register_blueprint(match_bp, url_prefix='/api/match')

    # health route
    @app.route('/')
    def home():
        return jsonify({'message': 'Resume-to-Job Fit Scorer Backend Running 🚀'})

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # create tables if they don't exist
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
