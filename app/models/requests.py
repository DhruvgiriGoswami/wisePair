from app import db
from app.models.base import BaseModel

class RequestStatus:
    """Constants for request status"""
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

class MentorRequest(BaseModel):
    """Model for team requests to professors for mentorship"""
    __tablename__ = 'mentor_requests'
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'), nullable=False)
    status = db.Column(db.String(20), default=RequestStatus.PENDING, nullable=False)
    message = db.Column(db.Text, nullable=True)  # Optional message to professor
    
    # Relationships
    team = db.relationship('Team', back_populates='mentor_requests')
    professor = db.relationship('Professor', back_populates='mentor_requests')
    
    __table_args__ = (
        db.UniqueConstraint('team_id', 'professor_id', name='unique_team_professor'),
    )
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'team_id': self.team_id,
            'professor_id': self.professor_id,
            'status': self.status,
            'message': self.message,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SeniorMentorRequest(BaseModel):
    """Model for team requests to senior mentors"""
    __tablename__ = 'senior_mentor_requests'
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False)
    status = db.Column(db.String(20), default=RequestStatus.PENDING, nullable=False)
    message = db.Column(db.Text, nullable=True)  # Optional message to mentor
    
    # Relationships
    team = db.relationship('Team', back_populates='senior_mentor_requests')
    mentor = db.relationship('Mentor', back_populates='senior_mentor_requests')
    
    __table_args__ = (
        db.UniqueConstraint('team_id', 'mentor_id', name='unique_team_mentor'),
    )
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'team_id': self.team_id,
            'mentor_id': self.mentor_id,
            'status': self.status,
            'message': self.message,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 