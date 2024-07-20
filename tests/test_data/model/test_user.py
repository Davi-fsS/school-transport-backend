import pytest
from app.data.model.user_model import UserModel
from app.data.model.user_type_model import UserTypeModel
from app.data.helpers.errors.model_errors import EntityError

class TestUser:
    user_type: UserTypeModel

    def __init__(self):
        self.user_type = UserTypeModel(1, "Administrador")

    def test_user(self):
        user = UserModel(2, "Vpe8zNjmWqUladEqAkdegYoaUXz2", "Davi", "davifssoares2002@gmail.com", "12345678910", "12345678910", "", user_type=self.user_type)
        assert type(user) is UserModel
    
    def test_user_uuid_is_not_string(self):
        with pytest.raises(EntityError.validate_field("uuid", str)):
            UserModel(2, 821, "Davi", "davifssoares2002@gmail.com", "12345678910", "12345678910", "", user_type=self.user_type)