# Import python packages
import streamlit as st
from streamlit import session_state as ss
import time
from helpers.fetch_configuration_table import fetch_configuration_table
from helpers.sync_changes_to_snowflake import sync_changes_to_snowflake
from helpers.secure_upload import secure_upload
from helpers.fetch_audit_logs import fetch_audit_logs
from helpers.fetch_user_connections import fetch_user_connections
from helpers.update_value import update_value

def admin_page(session):
   st.title("⚙️ Admin")
   user_id = st.session_state['user']
   # user_role = get_user_role()
   # if user_id not in ('SVC_DEV_DATA_STREAMLIT'):
   #     st.error("permission denied ")
   #     return
   data = fetch_configuration_table(session)
   edited_data = st.data_editor(data, use_container_width=True, num_rows="dynamic", key=ss.dek)
   st.button("Reset", on_click=update_value)
   if st.button("Save Changes"):
       sync_changes_to_snowflake(session, edited_data, data, user_id)
       st.success("Changes saved to Snowflake!")
       time.sleep(1) # Sleep for 1 seconds
       st.experimental_rerun()
   st.subheader("Secure File Upload")

   if st.button("Click Here to bulk import",help="click to import"):
       st.session_state.show_upload = True
   if st.session_state.get("show_upload", False):
       uploaded_file = st.text_area("Paste the contents of your CSV file here")
       if uploaded_file and st.button("Upload to the app !"):
           secure_upload(session, uploaded_file, user_id)
           st.session_state.show_upload = False
           time.sleep(1) # Sleep for 1 seconds
           st.experimental_rerun()
   # Audit Log display
   st.subheader("Audit Log")
   logs = fetch_audit_logs(session)
   filter_user = st.text_input("Filter by User ID")
   filter_date = st.date_input("Filter by Date", value=None)
   if filter_user:
       logs = logs[logs['user_id'] == filter_user]
   if filter_date:
       logs = logs[logs['date'].dt.date == filter_date]
   st.dataframe(logs)
   # Display user connections for the admin
   st.subheader("User Connections")
   user_connections = fetch_user_connections(session)
   st.dataframe(user_connections)