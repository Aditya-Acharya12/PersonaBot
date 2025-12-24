from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from bson import ObjectId

class UserCreate(BaseModel):
    name: Optional[str] 
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: Optional[str]
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class PersonaCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PersonaOut(BaseModel):
    id: str 
    user_id: str 
    name: str
    description: Optional[str] = None
