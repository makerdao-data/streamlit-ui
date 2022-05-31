import snowflake.connector

SNOWFLAKE_USERNAME=''
SNOWFLAKE_PASSWORD=''
SNOWFLAKE_HOST=''
SNOWFLAKE_ACCOUNT=''
SNOWFLAKE_WAREHOUSE=''
SNOWFLAKE_ROLE=''
MAIN_DB=''
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