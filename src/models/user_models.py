from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    name: str 
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr

class PersonaCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PersonaOut(BaseModel):
    id: str 
    user_id: str 
    name: str
    description: Optional[str] = None
