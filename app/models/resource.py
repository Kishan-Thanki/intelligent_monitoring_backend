def resource_helper(resource) -> dict:
    return {
        "id": str(resource["_id"]),
        "name": resource["name"],
        "type": resource["type"],
        "description": resource.get("description"),
        "owner_id": str(resource["owner_id"])
    }