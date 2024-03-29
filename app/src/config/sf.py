
import os
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE_USERNAME=os.getenv('SNOWFLAKE_USERNAME')
SNOWFLAKE_PASSWORD=os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_HOST=os.getenv('SNOWFLAKE_HOST')
SNOWFLAKE_ACCOUNT=os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_WAREHOUSE=os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_ROLE=os.getenv('SNOWFLAKE_ROLE')
MAIN_DB=os.getenv('MAIN_DB')
