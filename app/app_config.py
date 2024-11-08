# Import python packages
import streamlit as st
import logging
from streamlit import session_state as ss
import uuid
from snowflake.snowpark.context import get_active_session
from streamlit_extras.stylable_container import stylable_container
from helpers.record_user_connection import record_user_connection
from tabs.admin_page import admin_page
from tabs.user_page import user_page
from helpers.get_user_role import get_user_role
from helpers.detect_user import detect_user
from helpers.change_button_color import ChangeButtonColour
from streamlit_extras.app_logo import add_logo
from helpers.local_css import local_css
from helpers.footer import footer
import time


# create logger object 
logger = logging.getLogger("simple_logger")

# Manage page navigation
def main():

   add_logo("assets/logo.png", height=60)
   # List of admin roles
   # Write directly to the app
   st.title("Config Management User Application:coffee:")
   st.write(
       """Replace this example with your own CODE !
       **And if you're new to Streamlit and needs more help,** check
       out our easy-to-follow guides at
       [SG Streamlit Confluence](https://confluence.ids.saint-gobain.com/x/_4C1Dg).
       """
       )

   # Get the current credentials
   session = get_active_session()
#    st.write(session.get_current_role())
   st.session_state['user'] = detect_user()
   record_user_connection(session, st.session_state['user'])
   # Create de key
   if 'dek' not in ss:
      ss.dek = str(uuid.uuid4())
   
   ADMIN_ROLES = ["RF_DEV_DEVELOPER_STREAMLIT", "ACCOUNTADMIN"]
   st.sidebar.title("Navigation")
   user_id = st.session_state['user']
   user_role = get_user_role(session).strip('"\'')
   # Only show the admin page link if the user is an admin
   if user_role in ADMIN_ROLES:
       page = st.sidebar.selectbox("Go to", ["📜 Home", "⚙️ Admin"])
   else:
       page = st.sidebar.selectbox("Go to", ["📜 Home"])
   if page == "📜 Home":
       user_page(session)
   elif page == "⚙️ Admin":
      admin_page(session)
   # Apply custom CSS styles for header and button
   local_css("css/datafram_editor.css")
#    local_css("css/sidebar.css")
   
#    ChangeButtonColour('Save Changes', 'black', '#28a745') # button txt to find, colour to assign
#    ChangeButtonColour('Reset', '#c19af5', '#354b75') # button txt to find, colour to assign
#add footer
   file_path = "/tmp/appRoot/assets/logo.png"
   footer(session, file_path)
    
if __name__ == "__main__":
   main()