import streamlit as st
# Fetch the configuration table
def fetch_configuration_table(session):
   return session.table("configuration").to_pandas()