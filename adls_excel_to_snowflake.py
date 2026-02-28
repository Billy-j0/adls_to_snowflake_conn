import os
from io import BytesIO
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
import snowflake.connector
from dotenv import load_dotenv

print("Loading environment variables...")

# Load .env only if NOT running inside GitHub Actions
if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv()

ADLS_ACCOUNT = os.getenv("ADLS_ACCOUNT")
ADLS_KEY = os.getenv("ADLS_KEY")
FILE_SYSTEM = os.getenv("ADLS_CONTAINER")
FILE_PATH = os.getenv("ADLS_FILE_PATH")

SNOW_USER = os.getenv("SNOW_USER")
SNOW_PASSWORD = os.getenv("SNOW_PASSWORD")
SNOW_ACCOUNT = os.getenv("SNOW_ACCOUNT")
SNOW_DATABASE = os.getenv("SNOW_DATABASE")
SNOW_SCHEMA = os.getenv("SNOW_SCHEMA")
SNOW_WAREHOUSE = os.getenv("SNOW_WAREHOUSE")
SNOW_TABLE = os.getenv("SNOW_TABLE")

# READ EXCEL FROM ADLS
print("Connecting to Azure...")
service_client = DataLakeServiceClient(
    account_url=f"https://{ADLS_ACCOUNT}.dfs.core.windows.net",
    credential=ADLS_KEY
)

print(f"Downloading file from container...")
file_client = service_client.get_file_client(FILE_SYSTEM, FILE_PATH)
download = file_client.download_file()
excel_bytes = download.readall()

print("Reading Excel file into DataFrame...")
df = pd.read_excel(BytesIO(excel_bytes), engine="openpyxl")
print(f"Excel has {len(df)} rows and {len(df.columns)} columns.")

# SAVE CSV TEMP
csv_path = "/tmp/adls_file.csv"
print(f"Saving DataFrame to temporary CSV...")
df.to_csv(csv_path, index=False)

# LOAD INTO SNOWFLAKE
print("Connecting to Snowflake...")
conn = snowflake.connector.connect(
    user=SNOW_USER,
    password=SNOW_PASSWORD,
    account=SNOW_ACCOUNT,
    warehouse=SNOW_WAREHOUSE,
    database=SNOW_DATABASE,
    schema=SNOW_SCHEMA
)

cur = conn.cursor()

print(f"Truncating table...")
cur.execute(f"TRUNCATE TABLE {SNOW_TABLE}")

print("Uploading CSV file to Snowflake stage...")
cur.execute(f"PUT file://{csv_path} @%{SNOW_TABLE} OVERWRITE=TRUE")

print("Copying data into Snowflake table...")
cur.execute(f"""
COPY INTO {SNOW_TABLE}
FROM @%{SNOW_TABLE}/adls_file.csv
FILE_FORMAT = (
    TYPE = CSV
    FIELD_OPTIONALLY_ENCLOSED_BY='"'
    PARSE_HEADER = TRUE
)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
""")

print("Clean up snowflake internal stage...")
cur.execute(f"REMOVE @%{SNOW_TABLE}/adls_file.csv")

print("Load completed successfully!")