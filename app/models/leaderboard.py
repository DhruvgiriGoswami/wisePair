from app import db
from app.models.base import BaseModel

class Leaderboard(BaseModel):
    """Leaderboard model for tracking team progress and rankings"""
    __tablename__ = 'leaderboards'
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False, unique=True)
    meetings_done = db.Column(db.Integer, default=0)
    tasks_done = db.Column(db.Integer, default=0)
    mentor_feedback_count = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    
    # Relationships
    team = db.relationship('Team', back_populates='leaderboard')
    
    def recalculate_score(self):
        """Recalculate the total score based on other metrics"""
        self.total_score = self.meetings_done + self.tasks_done + self.mentor_feedback_count
        return self.total_score
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'meetings_done': self.meetings_done,
            'tasks_done': self.tasks_done,
            'mentor_feedback_count': self.mentor_feedback_count,
            'total_score': self.total_score,
            'updated_at': self.updated_at.isoformat()
        }
        
    @classmethod
    def get_top_teams(cls, limit=5):
        """Get the top performing teams"""
        return cls.query.order_by(cls.total_score.desc()).limit(limit).all()
    
    @classmethod
    def get_bottom_teams(cls, limit=5):
        """Get the bottom performing teams"""
        return cls.query.order_by(cls.total_score.asc()).limit(limit).all() 