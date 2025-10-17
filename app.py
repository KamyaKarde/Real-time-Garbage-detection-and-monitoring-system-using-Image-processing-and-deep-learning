import os
import pandas as pd
import streamlit as st
from glob import glob
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Garbage Monitoring", layout="wide")
st.title("🗑️ Real-time Garbage Monitoring")

CSV_PATH = "detections.csv"
SNAPSHOT_DIR = "latest_snapshots"

# Auto-refresh every 5 seconds
count = st_autorefresh(interval=5000, limit=None, key="auto_refresh")

# Load CSV
if not os.path.exists(CSV_PATH):
    st.warning("⚠️ No detections yet. Run the detection script first.")
else:
    try:
        df = pd.read_csv(CSV_PATH)
        if df.empty:
            st.info("Detections file is empty.")
        else:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("📷 Latest Snapshots from All Videos")
                snapshots = sorted(glob(os.path.join(SNAPSHOT_DIR, "*.jpg")), key=os.path.getmtime)
                
                if snapshots:
                    # Determine number of columns (up to 4 side by side)
                    n_cols = min(len(snapshots), 4)
                    cols = st.columns(n_cols)
                    
                    for idx, snap in enumerate(snapshots):
                        col_idx = idx % n_cols
                        cols[col_idx].image(snap, width=250)  # smaller width for side-by-side
                else:
                    st.info("No snapshots available yet.")

            with col2:
                st.subheader("📋 Recent Detections")
                st.dataframe(df.tail(10), use_container_width=True)

                st.subheader("📊 Summary")
                st.write(f"*Total Detections:* {len(df)}")
                st.bar_chart(df["label"].value_counts())

    except pd.errors.EmptyDataError:
        st.info("CSV file is empty. Waiting for detections...")











