from datetime import datetime

import streamlit as st

from exercises import exercise_library
from liftlog import load_log, log_workout, save_log

# to run "streamlit run app.py" in the terminal

if "page" not in st.session_state:
    st.session_state.page = "home"

if "draft" not in st.session_state:
    st.session_state.draft = []


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
        st.session_state.draft = []
        st.session_state.page = "home"
        st.rerun()

    st.title("Add workout")

    date = st.date_input("Date")
    exercise_names = [e["name"] for e in exercise_library]
    exercise = st.selectbox("Exercise", exercise_names)
    reps = st.number_input("Reps", min_value=1, value=5, step=1)
    weight = st.number_input("Weight (lbs)", min_value=0.0, value=135.0, step=5.0)
    notes = st.text_input("Notes")

    if st.button("Add set"):
        new_set = (int(reps), float(weight), notes)
        draft = st.session_state.draft

        if draft and draft[-1][0] == exercise:
            # same exercise as last entry → append another set
            name, sets = draft[-1]
            sets.append(new_set)
            draft[-1] = (name, sets)
        else:
            # different exercise → start a new (name, [set]) pair
            draft.append((exercise, [new_set]))

        st.rerun()

    if st.session_state.draft:
        st.subheader("Draft workout")
        rows = []
        for exercise_name, sets in st.session_state.draft:
            for i, (r, w, n) in enumerate(sets, start=1):
                rows.append({
                    "exercise": exercise_name,
                    "set": i,
                    "reps": r,
                    "weight": w,
                    "notes": n,
                })
        st.dataframe(rows, hide_index=True)

        if st.button("Save workout", type="primary"):
            workout_date = datetime.combine(date, datetime.min.time())
            df = load_log()
            df = log_workout(df, workout_date, st.session_state.draft)
            save_log(df)
            st.session_state.draft = []
            st.session_state.page = "home"
            st.rerun()
    else:
        st.caption("No sets added yet.")


if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "form":
    show_form()
