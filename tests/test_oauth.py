from src.scope.adapters.oauth.requester import OAuthRequester
from src.scope.adapters.oauth.provider import OAuthProvider
from src.scope.service_layer import services
from urllib.parse import urlencode


class FakeOAuthProvider(OAuthProvider):
    code_url = "http://provider.org/api/oauth/authorize"
    scopes = ['test_scope']
    token_url = 'http://provider.org/api/oauth/token'

    def _get_auth_code_redirect_uri(self):
        params = {
            'response_type': 'code',
            'client_id': 'test_client_id',
            'redirect_uri': 'http://test.org/callback',
            'state': 'test_state',
            'scope': 'test_scope'
        }
        return f"{self.code_url}?{urlencode(params)}"


class TestOAuth:
    def test_requester_returns_redirect_to_oauth_provider(self):
        fake_provider = FakeOAuthProvider()
        r = OAuthRequester(fake_provider)
        assert r.get_auth_code_redirect_uri() == 'http://provider.org/api/oauth/authorize?response_type=code&client_id=test_client_id&redirect_uri=http%3A%2F%2Ftest.org%2Fcallback&state=test_state&scope=test_scope'

    def test_service_returns_redirect_to_oauth_provider(self):
        fake_provider = FakeOAuthProvider()
        redirect_to_oauth = services.get_oauth_redirect(fake_provider)
        assert redirect_to_oauth == 'http://provider.org/api/oauth/authorize?response_type=code&client_id=test_client_id&redirect_uri=http%3A%2F%2Ftest.org%2Fcallback&state=test_state&scope=test_scope'
