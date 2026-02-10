import psycopg2
from src.utils.helpers import get_connection_config
import pymysql

def get_connection(name="source_db"):
    cfg = get_connection_config(name)

    return psycopg2.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        dbname=cfg["dbname"],
        user=cfg["user"],
        password=cfg["password"],
    )


def get_mysql_connection(name="source_db"):
    cfg = get_connection_config(name)
    return pymysql.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        database=cfg["dbname"],
        user=cfg["user"],
        password=cfg["password"],
    )