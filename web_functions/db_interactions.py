import pandas as pd
from sqlalchemy import create_engine
import pg8000
from dotenv import load_dotenv
import os

load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
engine = create_engine(f"postgresql+pg8000://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")

def read_table(schema, table, index=None):
    return pd.read_sql_table(table, engine, index_col=index, schema=schema)