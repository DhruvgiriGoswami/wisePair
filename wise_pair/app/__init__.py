from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='development'):
    """Factory for creating the Flask application"""
    from app.config import config_by_name
    
    # Initialize app
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Health check endpoint for container monitoring
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.teams import teams_bp
    from app.routes.mentors import mentors_bp
    from app.routes.professors import professors_bp
    from app.routes.meetings import meetings_bp
    from app.routes.leaderboard import leaderboard_bp
    from app.routes.files import files_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(teams_bp, url_prefix='/api/teams')
    app.register_blueprint(mentors_bp, url_prefix='/api/mentors')
    app.register_blueprint(professors_bp, url_prefix='/api/professors')
    app.register_blueprint(meetings_bp, url_prefix='/api/meetings')
    app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')
    app.register_blueprint(files_bp, url_prefix='/api/files')
    
    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    
    return app 