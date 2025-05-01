from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.file import File
from app.models.student import Student
from app.models.team import Team
from app.models.idea import Idea
from app.services.file_service import validate_file_upload, upload_file_to_minio
from app import db
import os

files_bp = Blueprint('files', __name__)

@files_bp.route('/upload/team', methods=['POST'])
@jwt_required()
def upload_team_file():
    """Upload a file associated with a team"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    if not student.team_id:
        return jsonify({'error': 'You are not in a team'}), 400
    
    team = Team.query.get(student.team_id)
    
    # Ensure request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    uploaded_file = request.files['file']
    
    # If user does not select a file
    if uploaded_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file
    validation_result = validate_file_upload(uploaded_file)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Upload file to MinIO
    storage_result = upload_file_to_minio(uploaded_file, f'team_{team.id}')
    if not storage_result['success']:
        return jsonify({'error': storage_result['message']}), 500
    
    # Create file record
    file = File(
        filename=storage_result['filename'],
        original_filename=uploaded_file.filename,
        file_type=os.path.splitext(uploaded_file.filename)[1],
        file_size=storage_result['size'],
        storage_path=storage_result['path'],
        public_url=storage_result.get('public_url'),
        team_id=team.id
    )
    
    file.save()
    
    return jsonify({
        'message': 'File uploaded successfully',
        'file': file.to_dict()
    }), 201

@files_bp.route('/upload/idea/<int:idea_id>', methods=['POST'])
@jwt_required()
def upload_idea_file(idea_id):
    """Upload a file associated with an idea"""
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    if not student.team_id:
        return jsonify({'error': 'You are not in a team'}), 400
    
    idea = Idea.query.get(idea_id)
    if not idea:
        return jsonify({'error': 'Idea not found'}), 404
    
    # Ensure the idea belongs to student's team
    if idea.team_id != student.team_id:
        return jsonify({'error': 'Access denied: idea does not belong to your team'}), 403
    
    # Ensure request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    uploaded_file = request.files['file']
    
    # If user does not select a file
    if uploaded_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file
    validation_result = validate_file_upload(uploaded_file)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Upload file to MinIO
    storage_result = upload_file_to_minio(uploaded_file, f'idea_{idea.id}')
    if not storage_result['success']:
        return jsonify({'error': storage_result['message']}), 500
    
    # Create file record
    file = File(
        filename=storage_result['filename'],
        original_filename=uploaded_file.filename,
        file_type=os.path.splitext(uploaded_file.filename)[1],
        file_size=storage_result['size'],
        storage_path=storage_result['path'],
        public_url=storage_result.get('public_url'),
        idea_id=idea.id
    )
    
    file.save()
    
    return jsonify({
        'message': 'File uploaded successfully',
        'file': file.to_dict()
    }), 201

@files_bp.route('/<int:file_id>', methods=['GET'])
@jwt_required()
def get_file(file_id):
    """Get file details including a public URL"""
    file = File.query.get(file_id)
    if not file:
        return jsonify({'error': 'File not found'}), 404
    
    # If file doesn't have a public URL, generate one
    if not file.public_url:
        file.generate_public_url()
        file.save()
    
    return jsonify(file.to_dict()), 200

@files_bp.route('/team/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team_files(team_id):
    """Get all files associated with a team"""
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    files = File.query.filter_by(team_id=team_id).all()
    return jsonify([file.to_dict() for file in files]), 200

@files_bp.route('/idea/<int:idea_id>', methods=['GET'])
@jwt_required()
def get_idea_files(idea_id):
    """Get all files associated with an idea"""
    idea = Idea.query.get(idea_id)
    if not idea:
        return jsonify({'error': 'Idea not found'}), 404
    
    files = File.query.filter_by(idea_id=idea_id).all()
    return jsonify([file.to_dict() for file in files]), 200 