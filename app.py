import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="6-Week Log", page_icon="💪")

st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("💪 6-Week Workout Tracker")

# Connect using the official connection name
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("log_form"):
    date = st.date_input("Date", datetime.now())
    week = st.selectbox("Week", range(1, 7))
    day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    ex = st.text_input("Exercise Name")
    m1 = st.number_input("Weight (lbs)", min_value=0)
    m2 = st.number_input("Reps", min_value=0)
    
    if st.form_submit_button("SAVE WORKOUT"):
        # Create the new entry
        new_data = pd.DataFrame([{"Date": date.strftime('%Y-%m-%d'), "Week": week, "Day": day, "Exercise": ex, "Metric1": m1, "Metric2": m2}])
        
        # Read existing data and add the new row
        existing_data = conn.read()
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        
        # Update the sheet
        conn.update(data=updated_df)
        st.success("Lift Recorded!")
        st.balloons()
        
