import streamlit as st
import pandas as pd
import random

# --- CONFIG ---
# Replace the URL below with your "Publish to Web" CSV link from Google Sheets
SHEET_URL = "YOUR_CSV_URL_HERE"

def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Build the nested dictionary from the Sheet
        tree = {}
        for _, row in df.iterrows():
            cat, sub, act = str(row['Category']), str(row['Sub-category']), str(row['Activity'])
            if cat not in tree: tree[cat] = {}
            if sub not in tree[cat]: tree[cat][sub] = []
            tree[cat][sub].append(act)
        return tree
    except:
        return {}

# --- UI ---
st.set_page_config(page_title="Evening Decider", page_icon="🌙")
st.title("🌙 Evening Decider")

data = load_data()

if not data:
    st.error("Could not load data. Check your Google Sheet link!")
else:
    # 1. Choose Category
    cat_list = list(data.keys())
    selected_cat = st.selectbox("What's the vibe?", ["-- Pick for me --"] + cat_list)

    if selected_cat == "-- Pick for me --":
        if st.button("🎯 SURPRISE ME", use_container_width=True):
            c = random.choice(cat_list)
            s = random.choice(list(data[c].keys()))
            a = random.choice(data[c][s])
            st.success(f"### {a}")
            st.caption(f"Category: {c} > {s}")
    else:
        # 2. Choose Sub-category
        sub_list = list(data[selected_cat].keys())
        selected_sub = st.selectbox(f"Narrow down {selected_cat}:", ["-- Pick for me --"] + sub_list)

        if st.button("🎰 GENERATE PLAN", use_container_width=True):
            st.balloons()
            if selected_sub == "-- Pick for me --":
                s = random.choice(sub_list)
                a = random.choice(data[selected_cat][s])
            else:
                a = random.choice(data[selected_cat][selected_sub])
            
            st.success(f"### {a}")
