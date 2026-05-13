import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIG ---
# Your specific Google Sheets CSV link is now integrated
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSyn_jmJv2ge4gQSquUXA0hCe3K__nL56vG9xV5HDUSW7ijncKSndy29bq3cHU95GTK2_sin07N88qR/pub?gid=0&single=true&output=csv"
MAX_HISTORY = 5 

def load_data():
    try:
        # Pull data from your Google Sheet
        df = pd.read_csv(SHEET_URL)
        
        # Clean up data: ensure 'Last Picked' exists and handle empty values
        if 'Last Picked' not in df.columns:
            df['Last Picked'] = None
        
        # Convert to datetime, turning errors/blanks into a very old date
        df['Last Picked'] = pd.to_datetime(df['Last Picked'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# --- UI SETUP ---
st.set_page_config(page_title="Evening Decider", page_icon="🌙")
st.title("🌙 Smart Evening Decider")
st.caption(f"Fresh ideas only — skipping your last {MAX_HISTORY} picks.")

df = load_data()

if df is not None:
    # --- ANTI-REPEAT LOGIC ---
    # Find the activities picked most recently based on the 'Last Picked' column
    recent_picks = df.sort_values(by='Last Picked', ascending=False).head(MAX_HISTORY)['Activity'].tolist()
    
    # Filter out those recent picks to ensure variety
    available_df = df[~df['Activity'].isin(recent_picks)]
    
    # Safety: If the list is too small to filter, use the whole thing
    if available_df.empty:
        available_df = df

    # --- SELECTION UI ---
    cat_list = sorted(available_df['Category'].unique().tolist())
    selected_cat = st.selectbox("What's the vibe?", ["-- Pick for me --"] + cat_list)

    if st.button("🎯 GENERATE TONIGHT'S PLAN", use_container_width=True):
        st.balloons()
        
        # Filter by category if one was selected
        if selected_cat == "-- Pick for me --":
            final_pool = available_df
        else:
            final_pool = available_df[available_df['Category'] == selected_cat]
        
        # Pick the winner
        winner = final_pool.sample(n=1).iloc[0]
        
        # Display Result with a nice visual border
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border: 2px solid #ff4b4b; border-radius: 10px; background-color: rgba(255, 75, 75, 0.05);">
            <h2 style="color: #ff4b4b; margin-bottom: 0;">Tonight we are doing:</h2>
            <h1 style="font-size: 3rem; margin-top: 10px;">{winner['Activity']}</h1>
            <p style="font-style: italic; color: #666;">{winner['Category']} > {winner['Sub-category']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Reminder to update the sheet for history tracking
        st.warning(f"**Action Required:** Open your Google Sheet and mark today's date in the 'Last Picked' column for **{winner['Activity']}** so it doesn't repeat tomorrow!")

else:
    st.info("👋 Welcome! Make sure your Google Sheet headers are exactly: Category, Sub-category, Activity, Last Picked.")
    
