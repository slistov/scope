from ..provider import OAuthProvider
# import google.oauth2.credentials
import google_auth_oauthlib.flow


class OAuthGoogleProvider(OAuthProvider):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            name='google',
            code_url='https://accounts.google.com/o/oauth2/v2/auth',
            scopes=['https://www.googleapis.com/auth/userinfo.email', 'openid'],
            token_url='https://oauth2.googleapis.com/token',
        )
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=self.scopes,
            redirect_uri=self._get_redirect_uri(),
        )

    def _get_authorize_uri(self):
        authorization_url, _ = self.flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=self.state
            )
        return authorization_url

    def _exchange_code_for_token(self, code):
        try:
            self.flow.fetch_token(code=code)
            self.credentials = self.flow.credentials
            return self.credentials
        except Exception as e:
            pass
