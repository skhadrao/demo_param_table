# Import python packages

# User detection placeholder function (expand for actual integration if needed)
def get_user_role(session):
   # df_current_user = session.sql(f"select current_role() as role")
   # st.write(df_current_user.first(1)[0]["USER"])
   # return df_current_user.first(1)[0]["ROLE"]
    return session.get_current_role()