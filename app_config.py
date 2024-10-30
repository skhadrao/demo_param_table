# Import python packages
import streamlit as st
from streamlit import session_state as ss
import uuid
from snowflake.snowpark.context import get_active_session
from helpers.record_user_connection import record_user_connection
from pages.admin_page import admin_page
from pages.user_page import user_page
from helpers.get_user_role import get_user_role
from helpers.detect_user import detect_user
from css.change_button_color import ChangeButtonColour

# Write directly to the app
st.title("Config Management User Application:coffee:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit and needs more help,** check
    out our easy-to-follow guides at
    [SG Streamlit Confluence](https://confluence.ids.saint-gobain.com/x/_4C1Dg).
    """
)

# Get the current credentials
session = get_active_session()

st.session_state['user'] = detect_user()
record_user_connection(st.session_state['user'])


# Create de key
if 'dek' not in ss:
    ss.dek = str(uuid.uuid4())


# Manage page navigation
def main():
   # List of admin roles
   ADMIN_ROLES = ["RF_DEV_DEVELOPER_STREAMLIT", "ACCOUNTADMIN"]
   st.sidebar.title("Navigation")
   user_id = st.session_state['user']
   user_role = get_user_role(session).strip('"\'')
   # Only show the admin page link if the user is an admin
   if user_role in ADMIN_ROLES:
       page = st.sidebar.selectbox("Go to", ["🏠 Home", "⚙️ Admin"])
   else:
       page = st.sidebar.selectbox("Go to", ["🏠 Home"])
   if page == "🏠 Home":
       user_page(session)
   elif page == "⚙️ Admin":
       admin_page(session)

# Apply custom CSS styles for header and button

st.markdown(
   """
<style>
   /* Style for the data_editor header columns */
   .stDataFrame thead {
       background-color: #007BFF !important;  /* Blue background */
       font-style: italic !important;          /* Italic text */
       color: white !important;                /* White text */
   }
</style>
   """,
   unsafe_allow_html=True
)

# cols = st.columns(4)
# cols[0].button('first button', key='b1')
# cols[1].button('second button', key='b2')
# cols[2].button('third button', key='b3')
# cols[3].button('fourth button', key='b4')

ChangeButtonColour('Save Changes', 'black', '#28a745') # button txt to find, colour to assign
ChangeButtonColour('Reset', '#c19af5', '#354b75') # button txt to find, colour to assign
    
if __name__ == "__main__":
   main()