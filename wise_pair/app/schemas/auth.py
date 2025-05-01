from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class StudentRegistrationSchema(BaseModel):
    """Schema for student registration"""
    name: str = Field(..., min_length=3, max_length=100)
    roll_no: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)
    year: int = Field(..., ge=1, le=5)
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v.strip()

class StudentLoginSchema(BaseModel):
    """Schema for student login"""
    email: EmailStr
    password: str = Field(..., min_length=1)

class ProfileUpdateSchema(BaseModel):
    """Schema for profile updates"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    year: Optional[int] = Field(None, ge=1, le=5)
    password: Optional[str] = Field(None, min_length=8)
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name must not be empty')
        return v.strip() if v else None 