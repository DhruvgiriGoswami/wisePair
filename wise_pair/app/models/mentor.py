from app import db
from app.models.base import BaseModel

class Mentor(BaseModel):
    """Mentor model representing a senior student mentor"""
    __tablename__ = 'mentors'
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)  # Year of study
    
    # Relationships
    mentored_teams = db.relationship('Team', back_populates='senior_mentor')
    senior_mentor_requests = db.relationship('SeniorMentorRequest', back_populates='mentor', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'year': self.year,
            'mentored_teams': [team.id for team in self.mentored_teams]
        } 