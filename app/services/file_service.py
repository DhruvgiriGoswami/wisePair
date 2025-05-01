import os
import uuid
from minio import Minio
from minio.error import S3Error
from werkzeug.utils import secure_filename
from flask import current_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'zip'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_upload(file):
    """Validate file upload"""
    # Check if file is allowed
    if not allowed_file(file.filename):
        return {
            'valid': False,
            'message': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }
    
    # Check file size (limit to 10MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer to beginning
    
    if file_size > 10 * 1024 * 1024:  # 10MB in bytes
        return {
            'valid': False,
            'message': 'File size exceeds the 10MB limit'
        }
    
    return {
        'valid': True
    }

def get_minio_client():
    """Get MinIO client from configuration"""
    try:
        return Minio(
            current_app.config['MINIO_ENDPOINT'],
            access_key=current_app.config['MINIO_ACCESS_KEY'],
            secret_key=current_app.config['MINIO_SECRET_KEY'],
            secure=False  # Set to True for HTTPS
        )
    except Exception as e:
        logger.error(f"Error creating MinIO client: {str(e)}")
        return None

def upload_file_to_minio(file, prefix='general'):
    """Upload file to MinIO and return storage information"""
    try:
        minio_client = get_minio_client()
        if not minio_client:
            return {
                'success': False,
                'message': 'Failed to connect to storage service'
            }
        
        # Get bucket name from config
        bucket_name = current_app.config['MINIO_BUCKET_NAME']
        
        # Check if bucket exists, if not create it
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            logger.info(f"Created bucket: {bucket_name}")
        
        # Secure the filename and add UUID to avoid collisions
        original_filename = secure_filename(file.filename)
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{prefix}/{str(uuid.uuid4())}{file_extension}"
        
        # Get file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        # Upload file
        minio_client.put_object(
            bucket_name,
            unique_filename,
            file,
            file_size,
            content_type=file.content_type
        )
        
        # Generate public URL (valid for 7 days)
        url = minio_client.presigned_get_object(
            bucket_name,
            unique_filename,
            expires=7*24*60*60  # 7 days in seconds
        )
        
        return {
            'success': True,
            'filename': unique_filename,
            'original_filename': original_filename,
            'size': file_size,
            'path': f"{bucket_name}/{unique_filename}",
            'public_url': url
        }
    
    except S3Error as e:
        logger.error(f"S3 Error uploading file: {str(e)}")
        return {
            'success': False,
            'message': f"Storage error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}"
        } 