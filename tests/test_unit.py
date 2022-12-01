from src.scope.domain import model
from src.scope.domain.security import verify_password


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


class TestAccount:
    def test_single_email_marked_as_main(self):
        account = model.Account(email="test@test.com", password="test_password")
        assert account.get_main_email() == "test@test.com"

    def test_hashed_password(self):
        account = model.Account(email="test@test.com", password="test_password")
        assert verify_password("test_password", account.get_hashed_password())
