from datetime import datetime

def validate_meeting_creation(data):
    """Validate meeting creation data"""
    required_fields = ['title', 'scheduled_date']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return {
                'valid': False,
                'message': f'Missing required field: {field}'
            }
    
    # Validate title
    if not data['title'] or len(data['title']) < 3:
        return {
            'valid': False,
            'message': 'Meeting title must be at least 3 characters long'
        }
    
    # Validate scheduled date
    try:
        scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        
        # Check if date is in the future
        if scheduled_date < datetime.now():
            return {
                'valid': False,
                'message': 'Meeting date must be in the future'
            }
    except (ValueError, TypeError):
        return {
            'valid': False,
            'message': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
        }
    
    # Validate professor or mentor is provided
    if 'professor_id' not in data and 'mentor_id' not in data:
        return {
            'valid': True,
            'message': 'Note: Neither professor nor mentor specified for this meeting'
        }
    
    return {
        'valid': True
    } 