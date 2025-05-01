from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.mentor import Mentor
from app.models.student import Student
from app.models.team import Team
from app.models.requests import SeniorMentorRequest, RequestStatus
from app import db

mentors_bp = Blueprint('mentors', __name__)

@mentors_bp.route('', methods=['GET'])
@jwt_required()
def get_all_mentors():
    """Get all available mentors"""
    mentors = Mentor.query.all()
    return jsonify([mentor.to_dict() for mentor in mentors]), 200

@mentors_bp.route('/<int:mentor_id>', methods=['GET'])
@jwt_required()
def get_mentor(mentor_id):
    """Get mentor details"""
    mentor = Mentor.query.get(mentor_id)
    if not mentor:
        return jsonify({'error': 'Mentor not found'}), 404
    
    return jsonify(mentor.to_dict()), 200

@mentors_bp.route('/request', methods=['POST'])
@jwt_required()
def request_mentor():
    """Request a senior mentor for a team"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    if not student.team_id:
        return jsonify({'error': 'You are not in a team'}), 400
    
    team = Team.query.get(student.team_id)
    
    # Check if student is the team leader
    if team.leader_id != student.id:
        return jsonify({'error': 'Only team leader can request mentors'}), 403
    
    # Check if team already has a senior mentor
    if team.senior_mentor_id:
        return jsonify({'error': 'Team already has a senior mentor'}), 400
    
    data = request.get_json()
    if 'mentor_id' not in data:
        return jsonify({'error': 'Mentor ID is required'}), 400
    
    mentor = Mentor.query.get(data['mentor_id'])
    if not mentor:
        return jsonify({'error': 'Mentor not found'}), 404
    
    # Check if request already exists
    existing_request = SeniorMentorRequest.query.filter_by(
        team_id=team.id,
        mentor_id=mentor.id
    ).first()
    
    if existing_request:
        return jsonify({'error': 'Request already sent to this mentor'}), 400
    
    # Create the request
    mentor_request = SeniorMentorRequest(
        team_id=team.id,
        mentor_id=mentor.id,
        message=data.get('message')
    )
    
    mentor_request.save()
    
    # TODO: Implement email notification to mentor
    
    return jsonify({
        'message': 'Mentor request sent successfully',
        'request': mentor_request.to_dict()
    }), 201

@mentors_bp.route('/requests/<int:request_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_request(request_id):
    """Respond to a mentor request (accept or reject)"""
    # TODO: Implement mentor authentication
    # For now, we'll use student auth as a placeholder
    
    mentor_request = SeniorMentorRequest.query.get(request_id)
    if not mentor_request:
        return jsonify({'error': 'Request not found'}), 404
    
    data = request.get_json()
    if 'status' not in data or data['status'] not in [RequestStatus.ACCEPTED, RequestStatus.REJECTED]:
        return jsonify({'error': 'Valid status (accepted/rejected) is required'}), 400
    
    mentor_request.status = data['status']
    
    # If accepted, assign mentor to team
    if data['status'] == RequestStatus.ACCEPTED:
        team = Team.query.get(mentor_request.team_id)
        team.senior_mentor_id = mentor_request.mentor_id
    
    mentor_request.save()
    
    # TODO: Implement email notification to team
    
    return jsonify({
        'message': f'Request {data["status"]}',
        'request': mentor_request.to_dict()
    }), 200 