import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SNOW_USER = os.getenv("SNOW_USER")
SNOW_PASSWORD = os.getenv("SNOW_PASSWORD")
SNOW_ACCOUNT = os.getenv("SNOW_ACCOUNT")
SNOW_DATABASE = os.getenv("SNOW_DATABASE")
SNOW_SCHEMA = os.getenv("SNOW_SCHEMA")
SNOW_WAREHOUSE = os.getenv("SNOW_WAREHOUSE")

conn = snowflake.connector.connect(
    user=SNOW_USER,
    password=SNOW_PASSWORD,
    account=SNOW_ACCOUNT,
    warehouse=SNOW_WAREHOUSE,
    database=SNOW_DATABASE,
    schema=SNOW_SCHEMA
)

print("Connected successfully!")