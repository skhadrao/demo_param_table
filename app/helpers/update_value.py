import uuid
from streamlit import session_state as ss
def update_value():
    """
    Located on top of the data editor.
    """
    ss.dek = str(uuid.uuid4())  # triggers reset