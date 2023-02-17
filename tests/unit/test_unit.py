from src.scope.domain import model
from src.scope.domain.security import verify_password
from urllib.parse import urlparse, parse_qs


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


class TestUserSideAuthorization:
    def test_APIcall_returns_oauthProviderURL(self, test_client):
        """Must return redirect url

        App imports oauth_client_lib's router.
        The router's API:
        Gets param
            provider
        Ex.:
            /oauth/authorize?provider=google

        Returns
            oauth provider url
        Ex.:
            '"https://accounts.google.com/o/oauth2/v2/auth?
            response_type=code
            &client_id=655857588737-dvupl27ddl03qceusdli8q229s065hlh.apps.googleusercontent.com
            &redirect_uri=http://127.0.0.1:8000/api/oauth/callback
            &scope=https://www.googleapis.com/auth/userinfo.email+openid
            &state=some_state_code"'
        """
        response = test_client.get("/api/oauth/redirect?provider=google")
        assert response.ok

        parsed_url = urlparse(response.text)
        query_as_dict = parse_qs(parsed_url.query)
        assert set([
            "response_type",
            "client_id",
            "redirect_uri",
            "scope",
            "state",
        ]).issubset(query_as_dict)
