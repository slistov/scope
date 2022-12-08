class FakeOAuthProvider:
    code_url = "http://provider.org/api/oauth/authorize"
    scopes = ['test_scope']
    token_url = 'http://provider.org/api/oauth/token'

    def __init__(self, redirect_uri) -> None:
        self.redirect_uri = redirect_uri

    def get_redirect_to_oauth(self):
        return self.redirect_uri


class TestOAuth:
    def test_OAuthProvider_returns_redirect_to_oauth_provider(self):
        provider = OAuthProviders.Google(redirect_uri='http://test.org/callback')
        assert provider.get_redirect_to_oauth()