def validate_team_creation(data):
    """Validate team creation data"""
    required_fields = ['name']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return {
                'valid': False,
                'message': f'Missing required field: {field}'
            }
    
    # Validate team name
    if not data['name'] or len(data['name']) < 3:
        return {
            'valid': False,
            'message': 'Team name must be at least 3 characters long'
        }
    
    if len(data['name']) > 50:
        return {
            'valid': False,
            'message': 'Team name must be at most 50 characters long'
        }
    
    return {
        'valid': True
    }

def can_join_team(student, team):
    """Check if a student can join a team"""
    # Check if team is full
    if team.member_count >= 4:
        return {
            'can_join': False,
            'message': 'Team is already full'
        }
    
    # Check if team is locked
    if team.is_locked:
        return {
            'can_join': False,
            'message': 'Team is locked and not accepting new members'
        }
    
    # Additional rules can be added here
    # For example, checking if student's year matches team requirements
    
    return {
        'can_join': True
    } 