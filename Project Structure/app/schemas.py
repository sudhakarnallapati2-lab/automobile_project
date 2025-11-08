from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str   # NEW

class UserLogin(BaseModel):
    email: str
    password: str
