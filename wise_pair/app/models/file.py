from app import db
from app.models.base import BaseModel

class File(BaseModel):
    """Model for file uploads"""
    __tablename__ = 'files'
    
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    storage_path = db.Column(db.String(500), nullable=False)  # Path in MinIO/S3
    public_url = db.Column(db.String(500), nullable=True)  # Optional public URL
    
    # Foreign Keys - can be associated with either a team or an idea
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('ideas.id'), nullable=True)
    
    # Relationships
    team = db.relationship('Team', back_populates='files')
    idea = db.relationship('Idea', back_populates='files')
    
    def generate_public_url(self, expiry_days=7):
        """Generate a public URL for the file (to be implemented in service layer)"""
        # This is just a placeholder - implementation will be in file service
        pass
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'public_url': self.public_url,
            'team_id': self.team_id,
            'idea_id': self.idea_id,
            'created_at': self.created_at.isoformat()
        } 