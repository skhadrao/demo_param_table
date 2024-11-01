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

def user_page(session):
   st.title("🏠 Home")
   user_id = st.session_state['user']
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
           progress_text = "Operation in progress. Please wait."
           my_bar = st.progress(0, text=progress_text)
           secure_upload(session, uploaded_file, user_id)
           st.session_state.show_upload = False
           my_bar.progress(100, text=progress_text)
           time.sleep(1) # Sleep for 1 seconds
           my_bar.empty()

           st.experimental_rerun()