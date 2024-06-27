import pytest
from app.data.model.user_model import User
from app.data.model.user_type_model import UserType
from app.data.helpers.errors.model_errors import EntityError

class TestUser:
    user_type: UserType

    def __init__(self, user_type: UserType):
        self.user_type = UserType(1, "Administrador")

    def test_user(self):
        user = User(2, "Vpe8zNjmWqUladEqAkdegYoaUXz2", "Davi", "davifssoares2002@gmail.com", "12345678910", "12345678910", "", user_type=self.user_type)
        assert type(user) is User
    
    def test_user_uuid_is_not_string(self):
        with pytest.raises(EntityError.validate_field("uuid", str)):
            User(2, 821, "Davi", "davifssoares2002@gmail.com", "12345678910", "12345678910", "", user_type=self.user_type)