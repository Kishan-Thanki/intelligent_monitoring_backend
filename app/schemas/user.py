from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=6, example="securepassword123")
    role: UserRole = Field(UserRole.USER, example="user")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="securepassword123")

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id", description="MongoDB ObjectId as string")
    email: EmailStr
    role: UserRole

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "60d0fe4f6a73c3001f2d34a5",
                "email": "testuser@example.com",
                "role": "user"
            }
        }