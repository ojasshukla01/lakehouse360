# 📊 Lakehouse360: End-to-End Data Engineering & Interactive Analytics Platform

**Lakehouse360** is a modular, open-source data engineering and analytics project built to demonstrate a complete pipeline from raw data ingestion to insightful interactive dashboards using only open-source tools like Python, DuckDB, and Streamlit.

---

## 📁 Project Structure

lakehouse360/
│
├── data/                     # Raw and intermediate data files
│   ├── json_files/           # Converted JSON records
│
├── output/
│   ├── cleaned_parquet/      # Cleaned Parquet outputs
│
├── transform/
│   ├── convert_to_json.py    # Converts CSV, JSONL, Parquet to unified JSON
│   ├── clean_and_export.py   # Cleans and exports to Parquet using DuckDB
│
├── validation/
│   ├── validate_data.py      # Validates data with Pydantic models
│   ├── profile_data.py       # Profiles JSON data using DuckDB
│
├── fixes/
│   ├── patch_orders_product_ids.py  # Fix missing product_id references in orders
│
├── analysis/
│   ├── duckdb_analytics.py   # Runs analytics using DuckDB and Pandas
│
├── streamlit_app/
│   ├── dashboard.py          # Interactive dashboard using Streamlit
│   ├── report_utils.py       # PDF report generation using fpdf
│
└── README.md                 # This file

---

## ✅ Features

- **Automatic data ingestion** from CSV, TSV, Parquet, and JSONL formats
- **Validation** with Pydantic to catch schema mismatches
- **Profiling** with DuckDB for column-level summaries
- **Cleaning & Transformation** using SQL within DuckDB
- **Advanced analytics** using Pandas and SQL queries
- **Streamlit Dashboard** for:
  - Complex filtering (multi-column, multi-select)
  - Visualizations (bar, line, pie charts via Plotly)
  - Summary metrics (row count, null count, etc.)
  - Export options:
    - Filtered data (CSV, Excel, JSON)
    - PDF reports with metadata and top records

---

## 🚀 Getting Started

### 1. Clone the repo

git clone https://github.com/ojasshukla01/lakehouse360.git
cd lakehouse360

### 2. Set up virtual environment

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

### 3. Run the Pipeline

# Convert data
python transform/convert_to_json.py

# Validate and clean
python validation/validate_data.py
python transform/clean_and_export.py

# Analyze
python analysis/duckdb_analytics.py

# Launch dashboard
streamlit run streamlit_app/dashboard.py

---

## 📦 Dependencies

- pandas
- duckdb
- streamlit
- fpdf
- openpyxl
- pyarrow
- plotly

Install them via:

pip install -r requirements.txt

---

## 📄 Author

Built by **Ojas Shukla**  
🎓 Data Engineer | Python | GCP | Streamlit | DuckDB | OSS Contributor

---

## 💡 Future Plans

- Scheduled automation with `cron` or `GitHub Actions`
- Dockerized deployment
- Integration with cloud storage (e.g., GCS/S3)
- Alerting and data quality monitoring

---

## 📬 Feedback

Found an issue or want to contribute? Feel free to open a pull request or create an issue!