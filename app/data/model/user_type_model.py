from abc import ABC
from data.helpers.errors.model_errors import EntityError

class UserType(ABC):
    id: int
    name: str

    def __init__(self, id: int, name: str):
        EntityError.validate_field(id, int)
        self.id = id

        EntityError.validate_field(name, str)
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }