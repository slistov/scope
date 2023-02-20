from src.scope.domain import model
from src.scope.domain.security import verify_password


class TestAccount:
    def test_single_email_marked_as_main(self):
        account = model.Account(
            email=model.Email("test@test.com", is_main=True),
            password="test_password"
        )
        assert account.get_main_email() == "test@test.com"

    def test_hashed_password(self):
        account = model.Account(
            email=model.Email("test@test.com"), 
            password="test_password"
        )
        assert verify_password("test_password", account.get_hashed_password())
