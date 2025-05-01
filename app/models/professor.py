from app import db
from app.models.base import BaseModel

class Professor(BaseModel):
    """Professor model representing a faculty mentor"""
    __tablename__ = 'professors'
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    accepted_team_count = db.Column(db.Integer, default=0)
    
    # Relationships
    mentored_teams = db.relationship('Team', back_populates='professor')
    mentor_requests = db.relationship('MentorRequest', back_populates='professor', cascade='all, delete-orphan')
    
    @property
    def can_accept_more_teams(self):
        """Check if professor can accept more teams (max 3)"""
        return self.accepted_team_count < 3
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'accepted_team_count': self.accepted_team_count,
            'can_accept_more_teams': self.can_accept_more_teams,
            'mentored_teams': [team.id for team in self.mentored_teams]
        } 