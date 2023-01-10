import os
import json
from dotenv import load_dotenv
load_dotenv()

import yaml
config = yaml.safe_load(open("config.yaml", mode="r", encoding="utf-8"))


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "postgres", "client"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


# LOGGING
ERROR_LOG_FILENAME = config['ERROR_LOG_FILENAME']


def get_oauth_params(provider_name):
    # def load_oauth_secrets():
    #     with open('client_secret.json') as f:
    #         secrets = json.load(f)["web"]
    #         return {
    #             "client_id": secrets["client_id"],
    #             "client_secret": secrets["client_secret"],
    #         }

    assert config['oauth']['providers'][provider_name]['scopes']
    assert config['oauth']['providers'][provider_name]['urls']
    providers = config['oauth']['providers']
    provider = providers[provider_name]
    scopes = provider['scopes']
    urls = provider['urls']
    return scopes, urls


def get_api_host():
    return os.environ['API_HOST']


def get_oauth_callback_URL():
    base_url = get_api_host()
    callback_path = config['oauth']['callback']
    return f"{base_url}{callback_path}"
