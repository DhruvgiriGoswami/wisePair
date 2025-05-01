from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.professor import Professor
from app.models.student import Student
from app.models.team import Team
from app.models.requests import MentorRequest, RequestStatus
from app import db

professors_bp = Blueprint('professors', __name__)

@professors_bp.route('', methods=['GET'])
@jwt_required()
def get_all_professors():
    """Get all available professors"""
    professors = Professor.query.all()
    return jsonify([professor.to_dict() for professor in professors]), 200

@professors_bp.route('/<int:professor_id>', methods=['GET'])
@jwt_required()
def get_professor(professor_id):
    """Get professor details"""
    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({'error': 'Professor not found'}), 404
    
    return jsonify(professor.to_dict()), 200

@professors_bp.route('/available', methods=['GET'])
@jwt_required()
def get_available_professors():
    """Get professors who can still accept more teams"""
    professors = Professor.query.filter(Professor.accepted_team_count < 3).all()
    return jsonify([professor.to_dict() for professor in professors]), 200

@professors_bp.route('/request', methods=['POST'])
@jwt_required()
def request_professor():
    """Request a professor for mentorship"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    if not student.team_id:
        return jsonify({'error': 'You are not in a team'}), 400
    
    team = Team.query.get(student.team_id)
    
    # Check if student is the team leader
    if team.leader_id != student.id:
        return jsonify({'error': 'Only team leader can request professors'}), 403
    
    # Check if team already has a professor
    if team.professor_id:
        return jsonify({'error': 'Team already has a professor mentor'}), 400
    
    data = request.get_json()
    if 'professor_id' not in data:
        return jsonify({'error': 'Professor ID is required'}), 400
    
    professor = Professor.query.get(data['professor_id'])
    if not professor:
        return jsonify({'error': 'Professor not found'}), 404
    
    # Check if professor can accept more teams
    if not professor.can_accept_more_teams:
        return jsonify({'error': 'Professor cannot accept more teams'}), 400
    
    # Check if request already exists
    existing_request = MentorRequest.query.filter_by(
        team_id=team.id,
        professor_id=professor.id
    ).first()
    
    if existing_request:
        return jsonify({'error': 'Request already sent to this professor'}), 400
    
    # Create the request
    mentor_request = MentorRequest(
        team_id=team.id,
        professor_id=professor.id,
        message=data.get('message')
    )
    
    mentor_request.save()
    
    # TODO: Implement email notification to professor
    
    return jsonify({
        'message': 'Professor mentorship request sent successfully',
        'request': mentor_request.to_dict()
    }), 201

@professors_bp.route('/requests/<int:request_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_request(request_id):
    """Respond to a mentorship request (accept or reject)"""
    # TODO: Implement professor authentication
    # For now, we'll use student auth as a placeholder
    
    mentor_request = MentorRequest.query.get(request_id)
    if not mentor_request:
        return jsonify({'error': 'Request not found'}), 404
    
    data = request.get_json()
    if 'status' not in data or data['status'] not in [RequestStatus.ACCEPTED, RequestStatus.REJECTED]:
        return jsonify({'error': 'Valid status (accepted/rejected) is required'}), 400
    
    mentor_request.status = data['status']
    
    # If accepted, assign professor to team and increment count
    if data['status'] == RequestStatus.ACCEPTED:
        professor = Professor.query.get(mentor_request.professor_id)
        
        # Double-check if professor can accept more teams
        if not professor.can_accept_more_teams:
            return jsonify({'error': 'Professor cannot accept more teams'}), 400
        
        team = Team.query.get(mentor_request.team_id)
        team.professor_id = mentor_request.professor_id
        
        # Increment accepted team count
        professor.accepted_team_count += 1
        db.session.commit()
    
    mentor_request.save()
    
    # TODO: Implement email notification to team
    
    return jsonify({
        'message': f'Request {data["status"]}',
        'request': mentor_request.to_dict()
    }), 200 