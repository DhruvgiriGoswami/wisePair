from app import db
from app.models.base import BaseModel

class Team(BaseModel):
    """Team model representing a hackathon team"""
    __tablename__ = 'teams'
    
    name = db.Column(db.String(100), nullable=False, unique=True)
    is_locked = db.Column(db.Boolean, default=False)  # Locked once team is full
    
    # Relationships
    leader_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    leader = db.relationship('Student', foreign_keys=[leader_id], back_populates='leading_team')
    
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'))
    professor = db.relationship('Professor', back_populates='mentored_teams')
    
    senior_mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'))
    senior_mentor = db.relationship('Mentor', back_populates='mentored_teams')
    
    # Team members (backref from Student model)
    members = db.relationship('Student', foreign_keys='Student.team_id', back_populates='team')
    
    # Ideas, meetings and other relationships
    ideas = db.relationship('Idea', back_populates='team', cascade='all, delete-orphan')
    meetings = db.relationship('Meeting', back_populates='team', cascade='all, delete-orphan')
    mentor_requests = db.relationship('MentorRequest', back_populates='team', cascade='all, delete-orphan')
    senior_mentor_requests = db.relationship('SeniorMentorRequest', back_populates='team', cascade='all, delete-orphan')
    leaderboard = db.relationship('Leaderboard', back_populates='team', uselist=False, cascade='all, delete-orphan')
    files = db.relationship('File', back_populates='team', cascade='all, delete-orphan')
    
    @property
    def member_count(self):
        """Get the number of team members"""
        return len(self.members)
    
    @property
    def is_full(self):
        """Check if the team has reached the maximum number of members (4)"""
        return self.member_count >= 4
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'is_locked': self.is_locked,
            'leader_id': self.leader_id,
            'professor_id': self.professor_id,
            'senior_mentor_id': self.senior_mentor_id,
            'member_count': self.member_count,
            'members': [member.to_dict() for member in self.members],
            'created_at': self.created_at.isoformat()
        } 