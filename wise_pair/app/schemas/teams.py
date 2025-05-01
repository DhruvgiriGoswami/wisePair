from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List

class TeamCreationSchema(BaseModel):
    """Schema for team creation"""
    name: str = Field(..., min_length=3, max_length=50)
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Team name must not be empty')
        return v.strip()

class TeamInviteSchema(BaseModel):
    """Schema for team invitations"""
    email: EmailStr

class TeamMemberSchema(BaseModel):
    """Schema for team members"""
    id: int
    name: str
    roll_no: str
    email: EmailStr
    year: int
    is_leader: bool

class TeamResponseSchema(BaseModel):
    """Schema for team response"""
    id: int
    name: str
    is_locked: bool
    leader_id: int
    professor_id: Optional[int] = None
    senior_mentor_id: Optional[int] = None
    member_count: int
    members: List[TeamMemberSchema]
    created_at: str 