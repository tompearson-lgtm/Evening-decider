import streamlit as st
import pandas as pd
import random

# --- CONFIG ---
# Using your specific Google Sheets CSV link
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSyn_jmJv2ge4gQSquUXA0hCe3K__nL56vG9xV5HDUSW7ijncKSndy29bq3cHU95GTK2_sin07N88qR/pub?gid=0&single=true&output=csv"

def load_data():
    try:
        # Cache-buster ensures it pulls fresh data from your Sheet every time
        df = pd.read_csv(f"{SHEET_URL}&cachebuster={random.randint(1,1000)}")
        
        # Ensure the 'Last Picked' column exists even if the Sheet is fresh
        if 'Last Picked' not in df.columns:
            df['Last Picked'] = None
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# --- UI SETUP ---
st.set_page_config(page_title="Evening Decider", page_icon="🌙")
st.title("🌙 Smart Evening Decider")
st.caption("Items marked with an 'x' in your sheet are currently hidden.")

df = load_data()

if df is not None:
    # --- SMART 'X' FILTERING ---
    # Rows where 'Last Picked' is empty are "Available"
    # Rows with an 'x', a date, or any text are "Played" and filtered out
    available_df = df[df['Last Picked'].isna()]
    
    # Safety: If you've 'x'ed everything, warn the user
    if available_df.empty:
        st.warning("🎯 All items have been played! Clear the 'x' marks in your Google Sheet to start a new rotation.")
        # Fallback to the full list so the app remains functional
        available_df = df 
    
    # --- SELECTION UI ---
    # Get a clean list of categories from the available items
    cat_list = sorted(available_df['Category'].unique().tolist())
    selected_cat = st.selectbox("What's the vibe?", ["-- Pick for me --"] + cat_list)

    if st.button("🎯 GENERATE TONIGHT'S PLAN", use_container_width=True):
        st.balloons()
        
        # Filter by category if one was selected
        if selected_cat == "-- Pick for me --":
            final_pool = available_df
        else:
            final_pool = available_df[available_df['Category'] == selected_cat]
        
        # Randomly pick the winner
        winner = final_pool.sample(n=1).iloc[0]
        
        # Display Result
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border: 2px solid #ff4b4b; border-radius: 10px; background-color: rgba(255, 75, 75, 0.05);">
            <h2 style="color: #ff4b4b; margin-bottom: 0;">Tonight we are doing:</h2>
            <h1 style="font-size: 2.5rem; margin-top: 10px;">{winner['Activity']}</h1>
            <p style="color: #666;">{winner['Category']} > {winner['Sub-category']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Instructions for the user
        st.info(f"✅ To hide this next time, put an 'x' next to **{winner['Activity']}** in your Google Sheet.")

else:
    st.error("Could not connect to your Google Sheet. Please check your CSV link in the code.")
    
