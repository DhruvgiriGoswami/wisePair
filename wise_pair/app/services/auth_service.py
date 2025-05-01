from email_validator import validate_email, EmailNotValidError

def validate_registration(data):
    """Validate student registration data"""
    required_fields = ['name', 'roll_no', 'email', 'password', 'year']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return {
                'valid': False,
                'message': f'Missing required field: {field}'
            }
    
    # Validate name
    if not data['name'] or len(data['name']) < 3:
        return {
            'valid': False,
            'message': 'Name must be at least 3 characters long'
        }
    
    # Validate roll number
    if not data['roll_no'] or len(data['roll_no']) < 3:
        return {
            'valid': False,
            'message': 'Roll number must be at least 3 characters long'
        }
    
    # Validate email
    try:
        valid_email = validate_email(data['email'])
        # Email is valid
    except EmailNotValidError as e:
        return {
            'valid': False,
            'message': f'Invalid email: {str(e)}'
        }
    
    # Validate password
    if not data['password'] or len(data['password']) < 8:
        return {
            'valid': False,
            'message': 'Password must be at least 8 characters long'
        }
    
    # Validate year
    try:
        year = int(data['year'])
        if year < 1 or year > 5:
            return {
                'valid': False,
                'message': 'Year must be between 1 and 5'
            }
    except (ValueError, TypeError):
        return {
            'valid': False,
            'message': 'Year must be a valid number'
        }
    
    return {
        'valid': True
    }

def validate_login(data):
    """Validate student login data"""
    required_fields = ['email', 'password']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return {
                'valid': False,
                'message': f'Missing required field: {field}'
            }
    
    # Validate email
    try:
        valid_email = validate_email(data['email'])
        # Email is valid
    except EmailNotValidError as e:
        return {
            'valid': False,
            'message': f'Invalid email: {str(e)}'
        }
    
    return {
        'valid': True
    } 