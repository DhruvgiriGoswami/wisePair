from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.meeting import Meeting, MeetingStatus
from app.models.student import Student
from app.models.team import Team
from app.services.meeting_service import validate_meeting_creation
from app import db
from datetime import datetime

meetings_bp = Blueprint('meetings', __name__)

@meetings_bp.route('', methods=['POST'])
@jwt_required()
def create_meeting():
    """Schedule a new meeting"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    if not student.team_id:
        return jsonify({'error': 'You are not in a team'}), 400
    
    team = Team.query.get(student.team_id)
    
    # Check if student is the team leader
    if team.leader_id != student.id:
        return jsonify({'error': 'Only team leader can schedule meetings'}), 403
    
    data = request.get_json()
    
    # Validate meeting data
    validation_result = validate_meeting_creation(data)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Parse datetime from string
    try:
        scheduled_date = datetime.fromisoformat(data['scheduled_date'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    # Create meeting
    meeting = Meeting(
        title=data['title'],
        description=data.get('description'),
        scheduled_date=scheduled_date,
        team_id=team.id,
        professor_id=data.get('professor_id'),
        mentor_id=data.get('mentor_id')
    )
    
    meeting.save()
    
    # TODO: Implement email notification to participants
    
    return jsonify({
        'message': 'Meeting scheduled successfully',
        'meeting': meeting.to_dict()
    }), 201

@meetings_bp.route('/<int:meeting_id>', methods=['GET'])
@jwt_required()
def get_meeting(meeting_id):
    """Get meeting details"""
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    
    return jsonify(meeting.to_dict()), 200

@meetings_bp.route('/team/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team_meetings(team_id):
    """Get all meetings for a team"""
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    meetings = Meeting.query.filter_by(team_id=team_id).order_by(Meeting.scheduled_date).all()
    return jsonify([meeting.to_dict() for meeting in meetings]), 200

@meetings_bp.route('/<int:meeting_id>/complete', methods=['POST'])
@jwt_required()
def complete_meeting(meeting_id):
    """Mark a meeting as completed and add feedback"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    
    # Check if student is in the team
    if not student.team_id or student.team_id != meeting.team_id:
        return jsonify({'error': 'Access denied: You are not in this team'}), 403
    
    # Check if meeting is already completed
    if meeting.status == MeetingStatus.COMPLETED:
        return jsonify({'error': 'Meeting is already marked as completed'}), 400
    
    data = request.get_json()
    feedback = data.get('feedback')
    
    # Mark meeting as completed and update feedback
    meeting.mark_completed(feedback)
    
    return jsonify({
        'message': 'Meeting marked as completed',
        'meeting': meeting.to_dict()
    }), 200

@meetings_bp.route('/<int:meeting_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_meeting(meeting_id):
    """Cancel a scheduled meeting"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    
    team = Team.query.get(meeting.team_id)
    
    # Only team leader can cancel meetings
    if team.leader_id != student.id:
        return jsonify({'error': 'Only team leader can cancel meetings'}), 403
    
    # Check if meeting is already completed or canceled
    if meeting.status != MeetingStatus.SCHEDULED:
        return jsonify({'error': f'Meeting is already {meeting.status}'}), 400
    
    meeting.status = MeetingStatus.CANCELED
    meeting.save()
    
    # TODO: Implement email notification to participants
    
    return jsonify({
        'message': 'Meeting canceled successfully',
        'meeting': meeting.to_dict()
    }), 200 