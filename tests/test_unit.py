from src.scope.domain import model


class TestEmailCheckCode:
    def test_generate_check_code(self):
        email = model.Email("test@test.com")
        check_code = email.get_check_code()
        assert check_code
        assert not email.is_checked
        assert True