# Fetch audit logs
def fetch_audit_logs(session):
   return session.table("audit_log").to_pandas()