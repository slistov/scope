from ..provider import OAuthProvider
# import google.oauth2.credentials
import google_auth_oauthlib.flow
from ....domain import security


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
            redirect_uri='http://127.0.0.1:8000/api/oauth/google',
        )

    def _get_auth_code_redirect_uri(self):
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

    def get_user_email(self):
        id_token = self.credentials.id_token
        try:
            token_data = security.decode_jwt(id_token, algorithm='RS256', verify_signature=True)
            email = token_data['email']
        except IndexError:
            pass
            return None
        except Exception as e:
            return None
        return email
