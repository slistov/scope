import requests


def get_provider_url(client, provider) -> str:
    r = client.get(f"/api/oauth/redirect?provider={provider}")
    if r.ok:
        return r.text
    return ''


def test_happy_path_google_auth(test_client):
    provider_url = get_provider_url(test_client, "google")
    assert provider_url
    provider_response = requests.get(provider_url, allow_redirects=True)

    parsed_url = urlparse(response.text)
    query_as_dict = parse_qs(parsed_url.query)
    assert set([
        "response_type",
        "client_id",
        "redirect_uri",
        "scope",
        "state",
    ]).issubset(query_as_dict)


def test_sideOAuthProvider_returns_token():
    return
