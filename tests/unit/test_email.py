from src.scope.domain import model


class TestEmailCheckCode:
    def test_generate_check_code(self):
        email = model.Email("test@test.com")
        code = email.get_check_code()
        assert code
        assert not email.is_checked

    def test_email_check(self):
        email = model.Email("test@test.com")
        code = email.get_check_code()
        assert email.confirm(code)
        assert email.is_checked

    def test_email_check_unlucky(self):
        email = model.Email("test@test.com")
        assert not email.confirm("wrong_code")
        assert not email.is_checked
