# ADLS to Snowflake Data Loader

## Overview

This project loads an Excel file stored in Azure Data Lake Storage (ADLS
Gen2) into a Snowflake table using Python.

### Process Flow

1.  Connect to Azure Data Lake Storage\
2.  Download Excel file\
3.  Load into Pandas DataFrame\
4.  Convert to CSV\
5.  Upload to Snowflake internal stage\
6.  Load into Snowflake table using COPY INTO

The workflow is automated using GitHub Actions.

------------------------------------------------------------------------

## Architecture

Azure Data Lake (Excel File)\
↓\
Python Script\
↓\
Snowflake Internal Stage\
↓\
Snowflake Table

------------------------------------------------------------------------

## Repository Structure

. ├── adls_excel_to_snowflake.py\
├── adls_connection_test.py\
├── requirements.txt\
├── .github/workflows/\
├── .gitignore\
└── README.md

------------------------------------------------------------------------

## Environment Variables

The script uses environment variables for configuration.

### Azure ADLS Variables

-   ADLS_ACCOUNT\
-   ADLS_KEY\
-   ADLS_CONTAINER\
-   ADLS_FILE_PATH

### Snowflake Variables

-   SNOW_USER\
-   SNOW_PASSWORD\
-   SNOW_ACCOUNT\
-   SNOW_DATABASE\
-   SNOW_SCHEMA\
-   SNOW_WAREHOUSE\
-   SNOW_TABLE

------------------------------------------------------------------------

## Local Setup

### 1. Clone the repository

git clone https://github.com/your-username/adls_to_snowflake_conn.git\
cd adls_to_snowflake_conn

### 2. Create virtual environment

python -m venv .venv\
source .venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Create a .env file (DO NOT COMMIT THIS FILE)

ADLS_ACCOUNT=your_value\
ADLS_KEY=your_value\
ADLS_CONTAINER=your_value\
ADLS_FILE_PATH=your_value

SNOW_USER=your_value\
SNOW_PASSWORD=your_value\
SNOW_ACCOUNT=your_value\
SNOW_DATABASE=your_value\
SNOW_SCHEMA=your_value\
SNOW_WAREHOUSE=your_value\
SNOW_TABLE=your_value

### 5. Run the script

python adls_excel_to_snowflake.py

------------------------------------------------------------------------

## GitHub Actions Automation

The workflow runs:

-   On push to main branch\
-   Or manually using workflow_dispatch

Secrets must be configured in:

Repository → Settings → Secrets and variables → Actions

------------------------------------------------------------------------

## Snowflake Load Strategy

The script performs:

-   TRUNCATE TABLE\
-   PUT command to upload file to internal stage\
-   COPY INTO to load data

This ensures a full refresh of the target table.

------------------------------------------------------------------------

## Security Best Practices

-   .env file is excluded using .gitignore\
-   Credentials are never hardcoded\
-   Secrets are stored in GitHub Actions Secrets\
-   Environment variables are injected during workflow execution

------------------------------------------------------------------------

## Dependencies

-   pandas\
-   openpyxl\
-   azure-storage-file-datalake\
-   snowflake-connector-python\
-   python-dotenv

Install using:

pip install -r requirements.txt

------------------------------------------------------------------------

## Author

William Johnson
