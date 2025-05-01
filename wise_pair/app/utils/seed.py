"""
Database seeding utility for development environments
"""

import random
import datetime
from werkzeug.security import generate_password_hash
from app import db
from app.models.student import Student
from app.models.professor import Professor
from app.models.mentor import Mentor
from app.models.team import Team
from app.models.leaderboard import Leaderboard

def seed_database():
    """Seed the database with initial data"""
    print("Seeding database...")
    
    # Clear existing data
    db.session.query(Leaderboard).delete()
    db.session.query(Team).delete()
    db.session.query(Mentor).delete()
    db.session.query(Professor).delete()
    db.session.query(Student).delete()
    db.session.commit()
    
    # Create students
    students = []
    for i in range(1, 21):
        student = Student(
            email=f"student{i}@example.com",
            password_hash=generate_password_hash("password"),
            first_name=f"Student{i}",
            last_name=f"LastName{i}",
            enrollment_id=f"E{100000+i}",
            major=random.choice(["Computer Science", "Electrical Engineering", "Information Technology", "Data Science"]),
            semester=random.choice([1, 2, 3, 4, 5, 6, 7, 8])
        )
        db.session.add(student)
        students.append(student)
    
    # Create professors
    professors = []
    for i in range(1, 6):
        professor = Professor(
            email=f"professor{i}@example.com",
            password_hash=generate_password_hash("password"),
            first_name=f"Professor{i}",
            last_name=f"LastName{i}",
            department=random.choice(["Computer Science", "Electrical Engineering", "Information Technology"]),
            expertise=random.choice(["AI/ML", "Web Development", "Database Systems", "Cybersecurity", "IoT"])
        )
        db.session.add(professor)
        professors.append(professor)
    
    # Create mentors (senior students)
    mentors = []
    for i in range(1, 11):
        mentor = Mentor(
            email=f"mentor{i}@example.com",
            password_hash=generate_password_hash("password"),
            first_name=f"Mentor{i}",
            last_name=f"LastName{i}",
            major=random.choice(["Computer Science", "Electrical Engineering", "Information Technology"]),
            expertise=random.choice(["Frontend", "Backend", "Mobile", "Data Science", "DevOps"]),
            semester=random.choice([7, 8])
        )
        db.session.add(mentor)
        mentors.append(mentor)
    
    # Create teams
    teams = []
    for i in range(1, 6):
        team_students = random.sample(students, min(4, len(students)))
        for student in team_students:
            students.remove(student)
        
        team = Team(
            name=f"Team {i}",
            description=f"This is team {i}'s project description",
            leader_id=team_students[0].id
        )
        
        # Add students to team
        for student in team_students:
            team.students.append(student)
            
        # Assign professor
        if professors:
            team.professor_id = random.choice(professors).id
            
        # Assign mentor
        if mentors:
            team.mentor_id = random.choice(mentors).id
            
        db.session.add(team)
        teams.append(team)
        
    # Create leaderboard entries
    for team in teams:
        leaderboard = Leaderboard(
            team_id=team.id,
            score=random.randint(50, 100),
            rank=0  # Will be calculated
        )
        db.session.add(leaderboard)
    
    db.session.commit()
    
    # Update ranks
    from sqlalchemy import desc
    leaderboard_entries = Leaderboard.query.order_by(desc(Leaderboard.score)).all()
    for i, entry in enumerate(leaderboard_entries):
        entry.rank = i + 1
    
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    # This allows running the script directly
    from flask import Flask
    from app.config import DevelopmentConfig
    
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    from app import db
    with app.app_context():
        seed_database() 