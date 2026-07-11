import streamlit as st

# to run "streamlit run app.py" in the terminal

st.title("LiftLog")
st.write("Hello, lifter!")

name = st.text_input("Your name")
if st.button("Say hi"):
    st.success(f"Hi, {name}!")