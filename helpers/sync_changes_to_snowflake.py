# Import python packages
from datetime import datetime
from helpers.log_action import log_action

# Sync changes to Snowflake from data_editor
def sync_changes_to_snowflake(session, new_df, original_df, user_id):
   # Identify inserted rows
   inserted_rows = new_df[~new_df['ID'].isin(original_df['ID'])]
   deleted_rows = original_df[~original_df['ID'].isin(new_df['ID'])]
   if not inserted_rows.empty:
       for index, row in inserted_rows.iterrows():
           session.sql(f"""
               INSERT INTO configuration (id, column1, column2, column3, column4, date_last_edited, edit_type)
               VALUES ('{row['ID']}', '{row['COLUMN1']}', '{row['COLUMN2']}', '{row['COLUMN3']}', '{row['COLUMN4']}', '{datetime.now()}', 'insert');
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
               SET column1 = '{new_row['COLUMN1']}', column2 = '{new_row['COLUMN2']}',
                   column3 = '{new_row['COLUMN3']}', column4 = '{new_row['COLUMN4']}',
                   date_last_edited = '{datetime.now()}', edit_type = 'update', id = '{new_row['ID']}'
               WHERE id = {new_row['ID']};
           """).collect()
           log_action(session, user_id, "update", "configuration", f"Updated row with id {new_row['ID']}")
   # update_value()