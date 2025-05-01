from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.leaderboard import Leaderboard

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('', methods=['GET'])
@jwt_required()
def get_all_leaderboard():
    """Get all teams in the leaderboard sorted by total score"""
    leaderboards = Leaderboard.query.order_by(Leaderboard.total_score.desc()).all()
    return jsonify([leaderboard.to_dict() for leaderboard in leaderboards]), 200

@leaderboard_bp.route('/top', methods=['GET'])
def get_top_teams():
    """Get top 5 teams in the leaderboard - public API, no auth required"""
    leaderboards = Leaderboard.get_top_teams(limit=5)
    return jsonify([leaderboard.to_dict() for leaderboard in leaderboards]), 200

@leaderboard_bp.route('/bottom', methods=['GET'])
@jwt_required()
def get_bottom_teams():
    """Get bottom 5 teams in the leaderboard - auth required"""
    leaderboards = Leaderboard.get_bottom_teams(limit=5)
    return jsonify([leaderboard.to_dict() for leaderboard in leaderboards]), 200

@leaderboard_bp.route('/team/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team_leaderboard(team_id):
    """Get leaderboard entry for a specific team"""
    leaderboard = Leaderboard.query.filter_by(team_id=team_id).first()
    
    if not leaderboard:
        return jsonify({'error': 'Leaderboard entry not found for this team'}), 404
    
    return jsonify(leaderboard.to_dict()), 200 