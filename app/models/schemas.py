from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    client = "client"
    auditor = "auditor"
    admin = "admin"

class UserCreate(BaseModel):
    username: str
    password: str
    role: Role

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
