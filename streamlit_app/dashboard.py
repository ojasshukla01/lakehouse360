import os
import duckdb
import pandas as pd
import streamlit as st
from fpdf import FPDF
from io import BytesIO
from pathlib import Path
import plotly.express as px

# ────────────── CONSTANTS ──────────────
PROJECT_NAME = "Lakehouse360 Dashboard"
PROJECT_DESCRIPTION = "Explore, filter, and export insights from Lakehouse360 datasets."
CREATOR_NAME = "Built by Ojas Shukla"
DATA_PATH = Path("output/cleaned_parquet")

# ────────────── LOAD DATA ──────────────
@st.cache_resource
def load_data():
    con = duckdb.connect()
    tables = {}
    for file in DATA_PATH.glob("*.parquet"):
        name = file.stem
        df = pd.read_parquet(file)
        con.register(name, df)
        tables[name] = df
    return tables, con

tables, con = load_data()
table_names = list(tables.keys())

# ────────────── SIDEBAR ──────────────
st.sidebar.title("🔎 Filters")
selected_table = st.sidebar.selectbox("Select Table", table_names)
df = tables[selected_table]
filter_cols = st.sidebar.multiselect("Columns to Filter", df.columns.tolist())

filter_values = {}
for col in filter_cols:
    unique_vals = df[col].dropna().unique().tolist()
    default_vals = unique_vals[:20]  # limit defaults to first 20 for speed
    filter_values[col] = st.sidebar.multiselect(f"{col}", unique_vals, default=default_vals)

# ────────────── FILTER DATA ──────────────
df_filtered = df.copy()
for col, vals in filter_values.items():
    df_filtered = df_filtered[df_filtered[col].isin(vals)]

# ────────────── PAGE HEADER ──────────────
st.title(PROJECT_NAME)
st.caption(PROJECT_DESCRIPTION)
st.subheader(f"📄 Table: `{selected_table}`")
st.info("⚠️ Showing only the first 100 rows for performance. Use export to get full data.")

# ────────────── SUMMARY ──────────────
col1, col2, col3 = st.columns(3)
col1.metric("Filtered Rows", len(df_filtered))
col2.metric("Columns", len(df_filtered.columns))
col3.metric("Missing Values", df_filtered.isnull().sum().sum())

st.divider()
st.dataframe(df_filtered.head(100))

# ────────────── VISUALIZATIONS ──────────────
st.subheader("📊 Visualizations")
numeric_cols = df_filtered.select_dtypes("number").columns
cat_cols = df_filtered.select_dtypes(["object", "category", "bool"]).columns

if len(numeric_cols) >= 1:
    st.markdown("#### 📊 Bar Chart (numeric)")
    y_axis = st.selectbox("Y-axis", numeric_cols, key="bar_y")
    fig_bar = px.bar(df_filtered.head(100), y=y_axis)
    st.plotly_chart(fig_bar, use_container_width=True)

if len(cat_cols) >= 1:
    st.markdown("#### 🥧 Pie Chart (categorical)")
    cat_axis = st.selectbox("Category", cat_cols, key="pie_cat")
    pie_df = df_filtered[cat_axis].value_counts().reset_index()
    pie_df.columns = [cat_axis, "count"]
    fig_pie = px.pie(pie_df, names=cat_axis, values="count")
    st.plotly_chart(fig_pie, use_container_width=True)

# ────────────── EXPORT SECTION ──────────────
st.subheader("📤 Export Options")

# CSV
st.download_button(
    "⬇️ CSV Export",
    df_filtered.to_csv(index=False),
    f"{selected_table}_filtered.csv",
    "text/csv"
)

# JSON
st.download_button(
    "⬇️ JSON Export",
    df_filtered.to_json(orient="records", indent=2).encode("utf-8"),
    f"{selected_table}_filtered.json",
    "application/json"
)

# Excel
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
    df_filtered.to_excel(writer, index=False, sheet_name="Filtered Data")
excel_buffer.seek(0)
st.download_button(
    "⬇️ Excel Export",
    excel_buffer.getvalue(),
    f"{selected_table}_filtered.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# PDF
def generate_pdf(df, title, table_name, applied_filters):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Table: {table_name}", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, f"Rows: {len(df)} | Columns: {len(df.columns)}", ln=True)

    if applied_filters:
        pdf.multi_cell(0, 10, f"Filters Applied:\n" + "\n".join([f"{k}: {v}" for k, v in applied_filters.items()]))

    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Top 10 Records:", ln=True)
    pdf.set_font("Arial", "", 9)
    for idx, row in df.head(10).iterrows():
        row_str = " | ".join(str(x) for x in row.values[:5])
        pdf.cell(0, 10, row_str[:100], ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, CREATOR_NAME, ln=True, align="C")

    return pdf.output(dest="S").encode("latin-1", "ignore")

applied_filters_summary = {k: v for k, v in filter_values.items() if v != df[k].unique().tolist()}
pdf_bytes = generate_pdf(df_filtered, "Lakehouse360 Report", selected_table, applied_filters_summary)
st.download_button("⬇️ PDF Export", pdf_bytes, f"{selected_table}_report.pdf", "application/pdf")
