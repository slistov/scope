from ..provider import OAuthProvider
import google.oauth2.credentials
import google_auth_oauthlib.flow


class OAuthGoogleProvider(OAuthProvider):
    name = 'google'
    code_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    scopes = ['https://www.googleapis.com/auth/userinfo.email']
    token_url = 'https://oauth2.googleapis.com/token'

    def __init__(self) -> None:
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=self.scopes,
            redirect_uri='http://127.0.0.1:8000/api/oauth/google'
            # app.url_path_for('api_google_callback')
        )
        super().__init__()

    def _get_auth_code_redirect_uri(self):
        authorization_url, state = self.flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            )
        return authorization_url

    def _exchange_code_for_token(self):
        pass
