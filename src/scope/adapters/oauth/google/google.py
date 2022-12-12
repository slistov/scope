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
            scopes=['https://www.googleapis.com/auth/userinfo.email'],
            token_url='https://oauth2.googleapis.com/token',
        )
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=self.scopes,
            redirect_uri='http://127.0.0.1:8000/api/oauth/google',
        )
        self.session = self.flow.authorized_session

    def _get_auth_code_redirect_uri(self):
        authorization_url, _ = self.flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=self.state
            )
        return authorization_url

    def _exchange_code_for_token(self):
        pass
