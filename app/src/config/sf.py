
import snowflake.connector
import os

SNOWFLAKE_USERNAME=os.getenv('SNOWFLAKE_USERNAME')
SNOWFLAKE_PASSWORD=os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_HOST=os.getenv('SNOWFLAKE_HOST')
SNOWFLAKE_ACCOUNT=os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_WAREHOUSE=os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_ROLE=os.getenv('SNOWFLAKE_ROLE')
MAIN_DB=os.getenv('MAIN_DB')

engine = snowflake.connector.connect(
    account=SNOWFLAKE_HOST,
    user=SNOWFLAKE_USERNAME,
    password=SNOWFLAKE_PASSWORD,
    warehouse=SNOWFLAKE_WAREHOUSE,
    role=SNOWFLAKE_ROLE,
    port=443,
    protocol='https'
)
sf = engine.cursor()