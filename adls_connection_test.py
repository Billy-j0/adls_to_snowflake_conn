from azure.storage.filedatalake import DataLakeServiceClient
import os
from dotenv import load_dotenv

load_dotenv()   # ← REQUIRED

service_client = DataLakeServiceClient(
    account_url=f"https://{os.getenv('ADLS_ACCOUNT')}.dfs.core.windows.net",
    credential=os.getenv("ADLS_KEY")
)

file_client = service_client.get_file_client(
    file_system=os.getenv("ADLS_CONTAINER"),
    file_path=os.getenv("ADLS_FILE_PATH")
)

download = file_client.download_file()
data = download.readall()

print("ADLS connection OK, bytes:", len(data))