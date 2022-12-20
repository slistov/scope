from typing import List
from urllib.parse import urlencode

import pytest

from src.scope.adapters.oauth.provider import OAuthProvider
from src.scope.adapters.oauth.requester import OAuthRequester
from src.scope.domain import model
from src.scope.service_layer import exceptions, services


class FakeOAuthProvider(OAuthProvider):
    def __init__(self) -> None:
        super().__init__(
            name='fake',
            code_url="http://provider.org/api/oauth/authorize",
            scopes=['test_scope'],
            token_url='http://provider.org/api/oauth/token',
            state='test_state'
        )

    def _get_authorize_uri(self):
        params = {
            'response_type': 'code',
            'client_id': 'test_client_id',
            'redirect_uri': 'http://test.org/callback',
            'state': self.state,
            'scope': self._get_scopes_str(),
        }
        return f"{self.code_url}?{urlencode(params)}"


class FakeDBAdapter:
    def __init__(
        self,
        authorizations: List[model.Authorization] = []
    ) -> None:
        self.authorizations = authorizations

    def get_authorization(self, state):
        for a in self.authorizations:
            if a.state == state:
                return a
        return None


class TestAuthorize:
    def test_requester_returns_redirect_to_oauth_provider(self):
        fake_provider = FakeOAuthProvider()
        r = OAuthRequester(fake_provider)
        assert r.get_authorize_uri() == 'http://provider.org/api/oauth/authorize?response_type=code&client_id=test_client_id&redirect_uri=http%3A%2F%2Ftest.org%2Fcallback&state=test_state&scope=test_scope'

    def test_service_returns_redirect_to_oauth_provider(self):
        fake_provider = FakeOAuthProvider()
        redirect_to_oauth = services.get_oauth_authorize_uri(fake_provider)
        assert redirect_to_oauth == 'http://provider.org/api/oauth/authorize?response_type=code&client_id=test_client_id&redirect_uri=http%3A%2F%2Ftest.org%2Fcallback&state=test_state&scope=test_scope'

    def test_authorize_saves_state(self):
        auth = model.Authorization(state='test_state')
        state = auth.state
        assert state
        assert not state == ''


class TestCallbackFromOAuthRecievesCode:
    def fake_db(self):
        a = model.Authorization(state='test_state')
        fake_db = FakeDBAdapter(authorizations=[a])
        return fake_db

    def test_callback_recieves_code_and_valid_state(self):
        fake_db = self.fake_db()
        services.validate_code_response(
            code='test_code',
            state='test_state',
            db_adapter=fake_db
        )
        assert fake_db.get_authorization('test_state').code == 'test_code'

    def test_callback_recieves_code_and_INVALID_state(self):
        fake_db = self.fake_db()
        with pytest.raises(exceptions.WrongStateOAuthException) as e:
            services.validate_code_response(
                code='test_code',
                state='!INVALID_test_state!',
                db_adapter=fake_db
            )
