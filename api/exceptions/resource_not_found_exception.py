from fastapi import HTTPException, status


class ResourceNotFoundException(HTTPException):
    def __init__(self, resource_name: str, resource_id: int | str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} with id {resource_id} not found",
        )
