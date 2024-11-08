# Import python packages
from datetime import datetime
# Log user actions to the audit log table
def log_action(session, user_id, action, table_name, details=""):
   session.sql(f"""
       INSERT INTO adm.audit_log (user_id, action, table_name, date, details)
       VALUES ('{user_id}', '{action}', '{table_name}', '{datetime.now()}', '{details}');
   """).collect()