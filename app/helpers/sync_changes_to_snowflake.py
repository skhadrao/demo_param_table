# Import python packages
from datetime import datetime
from helpers.log_action import log_action
import streamlit as st

# Sync changes to Snowflake from data_editor
def sync_changes_to_snowflake(session, new_df, original_df, user_id):
   # Identify inserted rows
   inserted_rows = new_df[~new_df['ID'].isin(original_df['ID'])]
   deleted_rows = original_df[~original_df['ID'].isin(new_df['ID'])]
   if not inserted_rows.empty:
       for index, row in inserted_rows.iterrows():
           st.write(row)
           session.sql(f"""
               INSERT INTO configuration (id, "user name", "first name", "last name", "DEPARTMENT", "ROLE", "table name", "QUERY", date_last_edited, edit_type)
               VALUES ('{row['ID']}', '{row['user name']}', '{row['first name']}', '{row['last name']}', '{row['DEPARTMENT']}', '{row['ROLE']}', '{row['table name']}', '{row['QUERY']}', '{datetime.now()}', 'insert');
           """).collect()
           
           log_action(session, user_id, "insert", "configuration", f"Inserted row with new data")
   # Identify deleted rows
   
   if not deleted_rows.empty:
       for index, row in deleted_rows.iterrows():
           session.sql(f"DELETE FROM configuration WHERE id = {row['ID']};").collect()
           log_action(session, user_id, "delete", "configuration", f"Deleted row with id {row['ID']}")
   # Identify updated rows
   for index, new_row in new_df.iterrows():
       original_row = original_df[original_df['ID'] == new_row['ID']]
       if not original_row.empty and not new_row.equals(original_row.squeeze()):
           session.sql(f"""
               UPDATE configuration
               SET "user name" = '{new_row['user name']}', "first name" = '{new_row['first name']}',
                   "last name" = '{new_row['last name']}', DEPARTMENT = '{new_row['DEPARTMENT']}',
                   ROLE = '{new_row['ROLE']}', "table name" = '{new_row['table name']}',
                   QUERY = '{new_row['QUERY']}',
                   date_last_edited = '{datetime.now()}', edit_type = 'update', id = '{new_row['ID']}'
               WHERE id = {new_row['ID']};
           """).collect()
           log_action(session, user_id, "update", "configuration", f"Updated row with id {new_row['ID']}")
   # update_value()