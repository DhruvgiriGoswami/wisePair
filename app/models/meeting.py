from app import db
from app.models.base import BaseModel

class MeetingStatus:
    """Constants for meeting status"""
    SCHEDULED = 'scheduled'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

class Meeting(BaseModel):
    """Meeting model for scheduling team reviews with professors/mentors"""
    __tablename__ = 'meetings'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default=MeetingStatus.SCHEDULED, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    
    # Foreign Keys
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    
    # Optional: can be either with professor or mentor
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'), nullable=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=True)
    
    # Relationships
    team = db.relationship('Team', back_populates='meetings')
    professor = db.relationship('Professor', backref='meetings')
    mentor = db.relationship('Mentor', backref='meetings')
    
    def mark_completed(self, feedback=None):
        """Mark meeting as completed and update feedback if provided"""
        self.status = MeetingStatus.COMPLETED
        if feedback:
            self.feedback = feedback
            
        # Update team's leaderboard stats
        if self.team and self.team.leaderboard:
            self.team.leaderboard.meetings_done += 1
            if feedback:
                self.team.leaderboard.mentor_feedback_count += 1
            self.team.leaderboard.recalculate_score()
            db.session.commit()
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'scheduled_date': self.scheduled_date.isoformat(),
            'status': self.status,
            'feedback': self.feedback,
            'team_id': self.team_id,
            'professor_id': self.professor_id,
            'mentor_id': self.mentor_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 