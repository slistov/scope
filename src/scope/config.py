import os
# import json
from dotenv import load_dotenv
load_dotenv()

import yaml
config = yaml.safe_load(open("config.yaml", mode="r", encoding="utf-8"))


def get_es_uri():
    host = os.environ.get("ELASTIC_HOST", "https://0.0.0.0")
    port = os.environ.get("ELASTIC_PORT", "9200")
    return f"{host}:{port}"

def get_es_user_credentials():
    user = os.environ.get("ELASTIC_USER", "elastic")
    password = os.environ.get("ELASTIC_PASSWORD", "Set ELASTIC_PASSWORD in .env file")
    return f"{user}", f"{password}"