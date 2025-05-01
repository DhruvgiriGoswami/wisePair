from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.student import Student
from app.models.team import Team

def team_leader_required(f):
    """
    Decorator to check if the current user is a team leader.
    Must be used after @jwt_required().
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        student_id = get_jwt_identity()
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        if not student.team_id:
            return jsonify({'error': 'You are not in a team'}), 403
        
        team = Team.query.get(student.team_id)
        
        if team.leader_id != student.id:
            return jsonify({'error': 'Only team leader can perform this action'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def team_member_required(f):
    """
    Decorator to check if the current user is a member of a team.
    Must be used after @jwt_required().
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        student_id = get_jwt_identity()
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        if not student.team_id:
            return jsonify({'error': 'You are not in a team'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def validate_json(schema):
    """
    Decorator to validate JSON request data against a schema.
    
    Args:
        schema: The schema class to validate against
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Missing JSON in request'}), 400
            
            data = request.get_json()
            
            try:
                # Validate data against schema
                validated_data = schema.model_validate(data)
                # Replace the request JSON with validated data
                request.validated_data = validated_data
            except Exception as e:
                return jsonify({'error': str(e)}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator 