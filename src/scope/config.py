import os
import json

import yaml
from dotenv import load_dotenv

load_dotenv()


config = yaml.safe_load(open("config.yaml", mode="r", encoding="utf-8"))

SECURITY_KEY = os.environ.get("SECURITY_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def get_postgres_uri():
    return os.environ.get("DB_URI")


def get_api_host():
    return config['API']['HOST']


def get_api_path():
    return config['API']['PATH']


def get_api_uri():
    host = get_api_host()
    path = get_api_path()
    return f'{host}{path}'


def get_oauth_redirect_uri():
    api_uri = get_api_uri()
    oauth_path = config['API']['OAUTH']['PATH']
    return f"{api_uri}{oauth_path}"
