import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📁 File Converter and Cleaner", layout="wide")
st.title("📁 File Converter and Cleaner")
st.write("Upload your CSV and Excel Files to clean the data and convert formats effortlessly 🚀")

files = st.file_uploader(
    "Upload CSV or Excel Files", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if files:
    for i, file in enumerate(files):
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.divider()
        st.subheader(f"🔍 {file.name} - Preview")
        st.dataframe(df.head())

        # Fill missing values
        if st.checkbox(f"Fill Missing Values - {file.name}", key=f"fillna_{i}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("✅ Missing values filled successfully!")
            st.dataframe(df.head())

        # Select columns
        selected_columns = st.multiselect(
            f"Select Columns - {file.name}",
            options=df.columns.tolist(),
            default=df.columns.tolist(),
            key=f"select_columns_{i}"
        )
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show Chart
        if st.checkbox(f"📊 Show Chart - {file.name}", key=f"chart_{i}"):
            numeric_df = df.select_dtypes(include="number")
            if not numeric_df.empty:
                st.subheader("Bar Chart")
                st.bar_chart(numeric_df)
            else:
                st.warning("⚠️ No numeric data available to plot.")

        # Format conversion
        format_choice = st.radio(
            f"Convert {file.name} to:", 
            ["CSV", "Excel"],
            key=f"format_{i}",
            horizontal=True
        )

        # File download
        if st.button(f"⬇️ Prepare Download - {file.name}", key=f"btn_{i}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.rsplit(".", 1)[0] + ".csv"
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.rsplit(".", 1)[0] + ".xlsx"

            output.seek(0)
            st.download_button(
                label="📥 Click to Download",
                data=output,
                file_name=new_name,
                mime=mime,
                key=f"download_button_{i}"
            )
            st.success("File is ready to download!")

