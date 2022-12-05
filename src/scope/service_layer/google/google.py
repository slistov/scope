from ..services import OAuthRequester


class OAuthGoogleRequester(OAuthRequester):
    code_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    scopes = ['https://www.googleapis.com/auth/userinfo.email']
    token_url = 'https://oauth2.googleapis.com/token'

    def _get_auth_code_redirect_uri(self):
        

    def _exchange_code_for_token(self):
        pass
