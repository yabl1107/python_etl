import os
import configparser
from pathlib import Path

_config = None

def load_config():
    global _config

    if _config is None:
        env = os.getenv("ENV", "dev")

        parser = configparser.ConfigParser()
        parser.read(Path("config.ini"))

        parser.env = env
        _config = parser

    return _config


def get_connection_config(name: str) -> dict:
    config = load_config()
    env = config.env

    section = f"{env}.{name}"
    raw = config[section]

    return {k: os.path.expandvars(v) for k, v in raw.items()}
