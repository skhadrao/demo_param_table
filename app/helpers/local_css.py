import streamlit as st

def local_css(file_name):
    with open(file_name) as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)