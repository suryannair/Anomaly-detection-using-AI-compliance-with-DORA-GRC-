import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

st.set_page_config(page_title="Anomaly Detection App", layout="wide")

st.title("🔍 AI-Powered Anomaly Detection for GRC/Compliance")

uploaded_file = st.file_uploader("Upload a file (Excel or CSV)", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("✅ File loaded successfully!")
        st.dataframe(df.head())

        # ---- Feature Engineering ---- #
        st.subheader("🔧 Feature Engineering")

        required_cols = ["UserID", "Time", "File", "Action", "FileSize_MB", "Sensitivity"]
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
        else:
            # Convert Time to datetime & extract hour
            df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
            df["Hour"] = df["Time"].dt.hour

            # Encode Sensitivity
            sensitivity_map = {"Low": 0, "Medium": 1, "High": 2}
            df["SensitivityEncoded"] = df["Sensitivity"].map(sensitivity_map)

            # Encode DeptMismatch if department columns are present
            if "Department" in df.columns and "OwnerDept" in df.columns:
                df["DeptMismatch"] = df["Department"] != df["OwnerDept"]
                df["DeptMismatch"] = df["DeptMismatch"].astype(int)
            else:
                df["DeptMismatch"] = 0  # Assume no mismatch if data is missing

            # Final features
            features = df[["FileSize_MB", "Hour", "SensitivityEncoded", "DeptMismatch"]].copy()

            # ---- Anomaly Detection ---- #
            st.subheader("🤖 Running Isolation Forest")
            model = IsolationForest(contamination=0.05, random_state=42)
            model.fit(features)

            df["AnomalyScore"] = model.decision_function(features)
            df["AnomalyLabel"] = model.predict(features)
            df["AnomalyLabel"] = df["AnomalyLabel"].apply(lambda x: 1 if x == -1 else 0)

            st.success("✅ Anomaly detection complete.")
            st.markdown("### 🔎 Top 10 Most Suspicious Entries")
            st.dataframe(df[df["AnomalyLabel"] == 1].sort_values("AnomalyScore").head(10))

            # ---- Download Results ---- #
            st.download_button(
                label="📥 Download Full Results (CSV)",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="anomaly_detection_results.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
