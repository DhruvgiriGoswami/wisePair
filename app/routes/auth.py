from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.student import Student
from app.services.auth_service import validate_registration, validate_login
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new student"""
    data = request.get_json()
    
    # Validate registration data
    validation_result = validate_registration(data)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Check if email or roll_no already exists
    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if Student.query.filter_by(roll_no=data['roll_no']).first():
        return jsonify({'error': 'Roll number already registered'}), 400
    
    # Create new student
    student = Student(
        name=data['name'],
        roll_no=data['roll_no'],
        email=data['email'],
        year=data['year']
    )
    student.password = data['password']
    
    # Save to database
    student.save()
    
    # Generate access token
    access_token = create_access_token(identity=student.id)
    
    return jsonify({
        'message': 'Registration successful',
        'access_token': access_token,
        'student': student.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a student"""
    data = request.get_json()
    
    # Validate login data
    validation_result = validate_login(data)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Find student by email
    student = Student.query.filter_by(email=data['email']).first()
    
    # Check if student exists and password is correct
    if not student or not student.verify_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate access token
    access_token = create_access_token(identity=student.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'student': student.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get the profile of the logged-in student"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(student.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update the profile of the logged-in student"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.get_json()
    
    # Update only allowed fields
    if 'name' in data:
        student.name = data['name']
    
    if 'year' in data:
        student.year = data['year']
    
    if 'password' in data:
        student.password = data['password']
    
    # Save changes
    student.save()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'student': student.to_dict()
    }), 200 