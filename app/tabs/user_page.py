# Import python packages
import streamlit as st
from streamlit import session_state as ss
from streamlit_extras.stylable_container import stylable_container
import time
from helpers.fetch_configuration_table import fetch_configuration_table
from helpers.sync_changes_to_snowflake import sync_changes_to_snowflake
from helpers.secure_upload import secure_upload
from helpers.fetch_audit_logs import fetch_audit_logs
from helpers.fetch_user_connections import fetch_user_connections
from helpers.update_value import update_value

def color_negative_red(value):
    if isinstance(value, int):
        color = 'red' if value < 4 else 'green'
        return f'background-color: {color}'
    return f'background-color: white'


def user_page(session):
   st.title("📜 Home")
   user_id = st.session_state['user']
   data = fetch_configuration_table(session)
   
   with stylable_container(
       key='df_editable',
       css_styles="""
           button {
               background-color: green;
               color: white;   
           }
           """,
   ):
       edited_data = st.data_editor(data, use_container_width=True, hide_index=True, num_rows="dynamic", key=ss.dek)
   
   with stylable_container(
       key='reset_button',
       css_styles="""
           button {
               background-color: #e30787;
               color: white;    
               width: 150px;
               display:flex;
               line-height: 30px;
               margin-left: auto;    
           }
           """,
   ):
       st.button("Reset", on_click=update_value)   
   with stylable_container(
       key='save_button',
       css_styles="""
           button {
               color: white
               font-weight: bold;
               width: 150px;
               display:flex;
               line-height: 30px;
               margin-left: 0px; 
               background: #008CBA;
               border-style: outset;
               border-color: #0066A2;  
           }
           """,
   ):
       
       if st.button("Save Changes to snowflake ❄"):
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

           st.experimental_rerun()