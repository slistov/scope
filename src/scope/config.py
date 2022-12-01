import yaml
import os
from dotenv import load_dotenv
load_dotenv()


config = yaml.safe_load(open("config.yaml", mode="r", encoding="utf-8"))


def get_postgres_uri():
    return os.environ.get("DB_URI")


def get_api_host():
    return config['API_HOST']