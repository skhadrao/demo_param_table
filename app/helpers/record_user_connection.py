# Import python packages
from datetime import datetime

# Record user's connection to the app
def record_user_connection(session, user_id):
   session.sql(f"""
       MERGE INTO adm.user_connections AS target
       USING (SELECT '{user_id}' AS user_id, '{datetime.now()}' AS last_connection) AS source
       ON target.user_id = source.user_id
       WHEN MATCHED THEN UPDATE SET last_connection = source.last_connection
       WHEN NOT MATCHED THEN INSERT (user_id, last_connection) VALUES (source.user_id, source.last_connection);
   """).collect()