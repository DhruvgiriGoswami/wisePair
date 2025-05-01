from app import db
from app.models.base import BaseModel

class Idea(BaseModel):
    """Model for team project ideas"""
    __tablename__ = 'ideas'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    problem_statement = db.Column(db.Text, nullable=True)
    solution_approach = db.Column(db.Text, nullable=True)
    
    # Foreign Keys
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    
    # Relationships
    team = db.relationship('Team', back_populates='ideas')
    files = db.relationship('File', back_populates='idea', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'problem_statement': self.problem_statement,
            'solution_approach': self.solution_approach,
            'team_id': self.team_id,
            'files': [file.to_dict() for file in self.files],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 