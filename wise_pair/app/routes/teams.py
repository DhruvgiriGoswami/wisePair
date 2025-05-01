from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.team import Team
from app.models.student import Student
from app.models.leaderboard import Leaderboard
from app.services.team_service import validate_team_creation, can_join_team
from app import db

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('', methods=['POST'])
@jwt_required()
def create_team():
    """Create a new team with the current student as leader"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Check if student is already in a team
    if student.team_id:
        return jsonify({'error': 'You are already in a team'}), 400
    
    # Check if student is already leading a team
    if student.leading_team:
        return jsonify({'error': 'You are already leading a team'}), 400
    
    data = request.get_json()
    
    # Validate team data
    validation_result = validate_team_creation(data)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Check if team name is already taken
    if Team.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Team name already taken'}), 400
    
    # Create new team
    team = Team(
        name=data['name'],
        leader_id=student.id
    )
    
    # Add student to team
    student.team_id = team.id
    
    # Create leaderboard entry for the team
    leaderboard = Leaderboard(team_id=team.id)
    
    # Save to database
    db.session.add(team)
    db.session.add(leaderboard)
    db.session.commit()
    
    return jsonify({
        'message': 'Team created successfully',
        'team': team.to_dict()
    }), 201

@teams_bp.route('/<int:team_id>/join', methods=['POST'])
@jwt_required()
def join_team(team_id):
    """Join an existing team"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Check if student is already in a team
    if student.team_id:
        return jsonify({'error': 'You are already in a team'}), 400
    
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    # Check if team is locked
    if team.is_locked:
        return jsonify({'error': 'Team is locked and not accepting new members'}), 400
    
    # Check if team is full
    if team.is_full:
        return jsonify({'error': 'Team is already full'}), 400
    
    # Check if student can join the team based on custom rules
    join_result = can_join_team(student, team)
    if not join_result['can_join']:
        return jsonify({'error': join_result['message']}), 400
    
    # Add student to team
    student.team_id = team.id
    student.save()
    
    # Lock team if full after joining
    if team.is_full:
        team.is_locked = True
        team.save()
    
    return jsonify({
        'message': 'Joined team successfully',
        'team': team.to_dict()
    }), 200

@teams_bp.route('/<int:team_id>/invite', methods=['POST'])
@jwt_required()
def invite_to_team(team_id):
    """Invite a student to join the team (placeholder for email functionality)"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    # Check if student is the team leader
    if team.leader_id != student.id:
        return jsonify({'error': 'Only team leader can send invites'}), 403
    
    # Check if team is locked
    if team.is_locked:
        return jsonify({'error': 'Team is locked and not accepting new members'}), 400
    
    # Check if team is full
    if team.is_full:
        return jsonify({'error': 'Team is already full'}), 400
    
    data = request.get_json()
    if 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    
    # Find student by email
    invite_student = Student.query.filter_by(email=data['email']).first()
    if not invite_student:
        return jsonify({'error': 'Student not found with this email'}), 404
    
    # Check if student is already in a team
    if invite_student.team_id:
        return jsonify({'error': 'Student is already in a team'}), 400
    
    # TODO: Implement actual email sending logic in a service
    # For now, just return success
    return jsonify({
        'message': f'Invitation sent to {data["email"]}',
        'team': team.to_dict()
    }), 200

@teams_bp.route('/<int:team_id>/lock', methods=['POST'])
@jwt_required()
def lock_team(team_id):
    """Lock a team to prevent new members from joining"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    # Check if student is the team leader
    if team.leader_id != student.id:
        return jsonify({'error': 'Only team leader can lock the team'}), 403
    
    # Lock the team
    team.is_locked = True
    team.save()
    
    return jsonify({
        'message': 'Team locked successfully',
        'team': team.to_dict()
    }), 200

@teams_bp.route('/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team(team_id):
    """Get team details"""
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    return jsonify(team.to_dict()), 200

@teams_bp.route('', methods=['GET'])
@jwt_required()
def get_all_teams():
    """Get all teams"""
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams]), 200

@teams_bp.route('/my-team', methods=['GET'])
@jwt_required()
def get_my_team():
    """Get the team of the logged-in student"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    if not student.team_id:
        return jsonify({'error': 'You are not in a team'}), 404
    
    team = Team.query.get(student.team_id)
    return jsonify(team.to_dict()), 200 