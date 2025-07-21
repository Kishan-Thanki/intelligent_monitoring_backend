from typing import Optional
from pydantic import BaseModel, Field

class ResourceCreate(BaseModel):
    name: str = Field(..., min_length=3, example="Production Server 1")
    type: str = Field(..., example="EC2 Instance")
    description: Optional[str] = Field(None, example="Main backend server for API services")

class ResourceResponse(BaseModel):
    id: str = Field(..., alias="_id", description="MongoDB ObjectId as string")
    name: str
    type: str
    description: Optional[str]
    owner_id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "60d0fe4f6a73c3001f2d34a6",
                "name": "Production Server 1",
                "type": "EC2 Instance",
                "description": "Main backend server",
                "owner_id": "60d0fe4f6a73c3001f2d34a5"
            }
        }

class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, example="Updated Server Name")
    type: Optional[str] = Field(None, example="New Instance Type")
    description: Optional[str] = Field(None, example="Updated description for the server")

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "name": "Updated Server Name",
                "description": "Updated description for the server"
            }
        }