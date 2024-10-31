# Fetch user connections
def fetch_user_connections(session):
   return session.table("user_connections").to_pandas()