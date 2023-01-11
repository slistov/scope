
from ..provider import OAuthProvider


class OAuthGoogleProvider(OAuthProvider):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            name='google',
            code_url='https://accounts.google.com/o/oauth2/v2/auth',
            scopes=[
                'https://www.googleapis.com/auth/userinfo.email',
                'openid'
            ],
            token_url='https://oauth2.googleapis.com/token',
            public_keys_url='https://www.googleapis.com/oauth2/v3/certs'
        )
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=self.scopes,
            redirect_uri=self._get_redirect_uri(),
        )

    def _get_authorize_uri_and_state(self):
        authorization_url, state = self.flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
            )
        return authorization_url, state

    def _exchange_code_for_token(self, code):
        try:
            self.flow.fetch_token(code=code)
            self.credentials = self.flow.credentials
            return self.credentials
        except Exception as e:
            pass
