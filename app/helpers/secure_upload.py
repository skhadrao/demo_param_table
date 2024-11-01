# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.types import StructType, IntegerType, StringType, TimestampType, StructField
from io import StringIO

# Handle secure file upload to Snowflake Stage
def secure_upload(session, file_contents, user_id):
   # stage_path = f"@SK_SNOWPARK_TEMP/{user_id}_upload_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
   schema = StructType([StructField("id", IntegerType()), StructField("column1", StringType()), StructField("column3", StringType()), StructField("column3", StringType()), StructField("column4", StringType()), StructField("date_last_edited", TimestampType()), StructField("edit_type", StringType())])
   upload_file_df = session.create_dataframe(pd.read_csv(StringIO(file_contents), sep=";", dtype={
    'id': 'int64',
    'column1': 'string',
    'column2': 'string',
    'column3': 'string',
    'column4': 'string',
    'date_last_edited': 'string',
    'edit_type': 'string'}, parse_dates=['DATE_LAST_EDITED']), schema)
   upload_file_df.write.mode("truncate").save_as_table("configuration")
   session.sql(f"UPDATE configuration SET edit_type = 'insert'").collect();
   session.sql(f"UPDATE configuration SET date_last_edited = CURRENT_TIMESTAMP()").collect();
   # session.file.put_stream(BytesIO(bytes(file_contents, encoding='utf8')), stage_path, auto_compress=False, overwrite=True)
   st.success(f"File successfully uploaded to:")