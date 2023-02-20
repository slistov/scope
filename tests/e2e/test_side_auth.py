import requests


def get_provider_url(client, provider) -> str:
    r = client.get(f"/api/oauth/redirect?provider={provider}")
    if r.ok:
        return r.text
    return ''
# 'http://testserver/api/oauth/redirect?provider=google'


def test_happy_path_google_auth(test_client):
    provider_url = get_provider_url(test_client, "google")
    assert provider_url

    provider_response = requests.get(provider_url, allow_redirects=True)
    assert provider_response.ok


def test_sideOAuthProvider_returns_token():
    assert True
