import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

# Page setup for mobile
st.set_page_config(page_title="6-Week Log", layout="centered")

# Huge buttons for sweaty thumbs
st.markdown("""
<style>
    div.stButton > button {width: 100%; height: 4em; font-size: 20px; background-color: #007bff; color: white; border-radius: 10px;}
    .stTextInput input {font-size: 18px !important;}
</style>
""", unsafe_allow_name=True)

st.title("🏋️‍♂️ Workout Tracker")

# 1. Day & Cycle Logic
days_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
today_name = days_map[datetime.now().weekday()]
week_num = st.sidebar.number_input("Current Cycle Week", 1, 6, 1)

st.info(f"**Week {week_num} | {today_name}**")

# 2. Connection to your Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Define Your 6-Week Routines
routines = {
    "Tuesday": ["Back Squat", "Bench Press", "Deadlift"],
    "Thursday": ["Overhead Press", "Pullups", "Dips"],
    "Saturday": ["Long Run (Zone 2)"],
    "Monday": ["Calisthenics/Core"],
    "Wednesday": ["Indoor Cycling"],
    "Friday": ["Yoga/Stretching"],
    "Sunday": ["Swimming"]
}

todays_exercises = routines.get(today_name, ["Rest & Mobility"])

# 4. Data Entry Form
with st.form("log_entry", clear_on_submit=True):
    log_data = []
    
    for ex in todays_exercises:
        st.subheader(ex)
        col1, col2, col3 = st.columns([1, 1, 0.5])
        with col1:
            w = st.text_input("Weight/Pace", key=f"{ex}_w", placeholder="lbs/min")
        with col2:
            r = st.text_input("Reps/Dist", key=f"{ex}_r", placeholder="count/mi")
        with col3:
            pr = st.checkbox("PR?", key=f"{ex}_pr")
        
        log_data.append({
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Week": week_num,
            "Day": today_name,
            "Exercise": ex,
            "Metric1": w,
            "Metric2": r,
            "PR": "Yes" if pr else "No"
        })

    if st.form_submit_button("SAVE WORKOUT"):
        new_entry = pd.DataFrame(log_data)
        existing_data = conn.read()
        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        conn.update(data=updated_df)
        st.success("Log Updated! Get some recovery.")
        