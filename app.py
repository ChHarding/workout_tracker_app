import streamlit as st

# to run "streamlit run app.py" in the terminal

if "page" not in st.session_state:
    st.session_state.page = "home"


def show_home():
    col1, col2 = st.columns([3, 1], vertical_alignment="center")

    with col1:
        st.title("LiftLog")

    with col2:
        if st.button("Log a workout", type="primary"):
            st.session_state.page = "form"
            st.rerun()

    st.write("Hello, lifter!")


def show_form():
    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()
    st.title("Add workout")


if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "form":
    show_form()
