from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.base import BaseModel

class Student(BaseModel):
    """Student model representing a hackathon participant"""
    __tablename__ = 'students'
    
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    year = db.Column(db.Integer, nullable=False)  # Year of study
    
    # Relationships
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', back_populates='members')
    
    # Team leadership - backref from Team model
    leading_team = db.relationship('Team', foreign_keys='Team.leader_id', back_populates='leader', uselist=False)
    
    @property
    def password(self):
        """Prevent password from being accessed"""
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """Set password to a hashed value"""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Check if password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'roll_no': self.roll_no,
            'email': self.email,
            'year': self.year,
            'team_id': self.team_id,
            'is_team_leader': self.leading_team is not None
        } 