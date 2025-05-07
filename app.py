import streamlit as st
import pandas as pd
import os

HISTORICAL_FILE = 'historical_ids.txt'

# Simple password gate
password = st.text_input("Enter password:", type="password")
if password != "team123":
    st.stop()

# Load existing IDs
def load_historical_ids():
    if os.path.exists(HISTORICAL_FILE):
        with open(HISTORICAL_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

# Save new ones
def update_historical_ids(new_ids):
    with open(HISTORICAL_FILE, 'a') as f:
        for id in new_ids:
            f.write(id + '\n')

st.title("🆔 ID Checker App")

# Manual Entry
st.subheader("Paste IDs (one per line)")
pasted_ids = st.text_area("Paste here:", height=150)

# File Upload
st.subheader("Or Upload ID Files (.txt or .csv)")
uploaded_files = st.file_uploader("Upload one or more files", type=['txt', 'csv'], accept_multiple_files=True)

# Collect new IDs
input_ids = set()

# From pasted text
if pasted_ids:
    input_ids.update(id.strip() for id in pasted_ids.splitlines() if id.strip())

# From uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            ids = df.iloc[:, 0].astype(str).str.strip()
        else:
            content = uploaded_file.read().decode('utf-8')
            ids = [line.strip() for line in content.splitlines() if line.strip()]
        input_ids.update(ids)

# Compare with historical
if input_ids:
    known_ids = load_historical_ids()
    new_ids = input_ids - known_ids

    if new_ids:
        st.success(f"✅ Found {len(new_ids)} new ID(s).")
        st.write("### New IDs:")
        st.dataframe(sorted(new_ids))

        if st.button("Update historical file with these IDs"):
            update_historical_ids(new_ids)
            st.success("✅ Historical IDs updated!")

        # Download button
        new_ids_df = pd.DataFrame(sorted(new_ids), columns=["New IDs"])
        st.download_button("Download new IDs", new_ids_df.to_csv(index=False), file_name="new_ids.csv")
    else:
        st.info("No new IDs found.")
