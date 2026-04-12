import os
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool

load_dotenv()


def get_conn_str():
    return f"""
    dbname={os.getenv('DATABASE_NAME')}
    user={os.getenv('DATABASE_USER')}
    password={os.getenv('DATABASE_PASSWORD')}
    host={os.getenv('DATABASE_HOST')}
    port={os.getenv('DATABASE_PORT')}
    """


def get_database_connection() -> AsyncConnectionPool:
    db_connection = AsyncConnectionPool(conninfo=get_conn_str())
    return db_connection
