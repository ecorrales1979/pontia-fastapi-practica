from .domain_exception import DomainException


class ResourceNotFoundException(DomainException):
    def __init__(self, resource_name: str, resource_id: int | str):
        super().__init__(
            f"{resource_name} with id {resource_id} not found",
        )
