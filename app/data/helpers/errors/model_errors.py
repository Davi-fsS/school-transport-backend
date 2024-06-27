from typing import Type

class EntityError:
    @staticmethod
    def validate_field(value, expected_type: Type):
        if not isinstance(value, expected_type):
            raise TypeError(f"Field {value} is not of type {expected_type.__name__}")
      

