from app.db import db
from typing import List
from bson import ObjectId
from app.models.resource import resource_helper
from app.dependencies import get_current_user, get_admin_user
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.resource import ResourceCreate, ResourceResponse, ResourceUpdate

router = APIRouter()

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource: ResourceCreate,
    current_user: dict = Depends(get_current_user)
):
    resource_data = resource.model_dump(exclude_unset=True)
    resource_data["owner_id"] = ObjectId(current_user["_id"])

    new_resource = await db.db.resources.insert_one(resource_data)
    created_resource = await db.db.resources.find_one({"_id": new_resource.inserted_id})

    if not created_resource:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create resource"
        )

    return resource_helper(created_resource)

@router.get("/", response_model=List[ResourceResponse])
async def get_resources(current_user: dict = Depends(get_current_user)):
    query = {}
    if current_user["role"] != "admin":
        query["owner_id"] = ObjectId(current_user["_id"])

    resources = []
    async for resource in db.db.resources.find(query):
        resources.append(resource_helper(resource))
    return resources

@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource_by_id(
    resource_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(resource_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Resource ID format")

    resource_doc = await db.db.resources.find_one({"_id": ObjectId(resource_id)})
    if not resource_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    if current_user["role"] != "admin" and str(resource_doc["owner_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return resource_helper(resource_doc)

@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: str,
    resource_update: ResourceUpdate,
    current_user: dict = Depends(get_admin_user)
):
    if not ObjectId.is_valid(resource_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Resource ID format")

    existing_resource = await db.db.resources.find_one({"_id": ObjectId(resource_id)})
    if not existing_resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    update_data = {k: v for k, v in resource_update.model_dump(exclude_unset=True).items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update provided")

    update_result = await db.db.resources.update_one(
        {"_id": ObjectId(resource_id)},
        {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found (or no changes needed)")

    updated_resource = await db.db.resources.find_one({"_id": ObjectId(resource_id)})
    return resource_helper(updated_resource)

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: str,
    current_user: dict = Depends(get_admin_user)
):
    if not ObjectId.is_valid(resource_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Resource ID format")

    delete_result = await db.db.resources.delete_one({"_id": ObjectId(resource_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return