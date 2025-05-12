import streamlit as st
import pandas as pd
import duckdb
from pathlib import Path
import plotly.express as px
import base64
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Lakehouse360 Dashboard", layout="wide")

# Paths
DATA_DIR = Path("output/cleaned_parquet")

# Summary metrics at the top
st.title("📊 Lakehouse360 Interactive Dashboard")
st.markdown("""
Welcome to the interactive analytics dashboard. This tool lets you:
- Explore insights from the Lakehouse360 platform
- Filter data across multiple dimensions
- Visualize trends and metrics dynamically
- Export results and generate reports
""")

# Load all data
@st.cache_resource

def load_data():
    con = duckdb.connect()
    tables = {}
    for file in DATA_DIR.glob("*.parquet"):
        name = file.stem
        df = pd.read_parquet(file)
        tables[name] = df
        con.register(name, df)
    return tables, con

tables, con = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
product_filter = st.sidebar.multiselect("Product Name", tables["products"]["product_name"].unique())
courier_filter = st.sidebar.multiselect("Courier", tables["deliveries"]["courier"].unique())

# Metrics Summary
st.subheader("📈 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{len(tables['customers']):,}")
col2.metric("Total Orders", f"{len(tables['orders']):,}")
col3.metric("Total Products", f"{len(tables['products']):,}")

# Revenue by Product
st.subheader("💰 Revenue by Product")
query = """
    SELECT 
        p.product_name, 
        SUM(o.quantity * o.price_per_unit) AS revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY revenue DESC
    LIMIT 10
"""
revenue_df = con.execute(query).df()
fig1 = px.bar(revenue_df, x="product_name", y="revenue", title="Top Products by Revenue")
st.plotly_chart(fig1, use_container_width=True)

# Download chart
buf1 = BytesIO()
fig1.write_image(buf1, format="png")
st.download_button("⬇️ Download Revenue Chart", buf1.getvalue(), "revenue_chart.png")

# Returns by Product
st.subheader("📦 Returns by Product")
returns_df = con.execute("""
    SELECT p.product_name, COUNT(*) AS num_returns
    FROM returns r
    JOIN orders o ON r.order_id = o.order_id
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY num_returns DESC
    LIMIT 10
""").df()
fig2 = px.bar(returns_df, x="product_name", y="num_returns", title="Most Returned Products")
st.plotly_chart(fig2, use_container_width=True)

buf2 = BytesIO()
fig2.write_image(buf2, format="png")
st.download_button("⬇️ Download Returns Chart", buf2.getvalue(), "returns_chart.png")

# Delivery Time
st.subheader("🚚 Average Delivery Delay by Courier")
delay_df = con.execute("""
    SELECT courier, 
           AVG(CAST(delivered_at AS TIMESTAMP) - CAST(estimated_arrival AS TIMESTAMP)) AS delay
    FROM deliveries
    WHERE delivered_at IS NOT NULL
    GROUP BY courier
""").df()
delay_df["delay_hours"] = delay_df["delay"].dt.total_seconds() / 3600
fig3 = px.bar(delay_df, x="courier", y="delay_hours", title="Avg Delivery Delay (hrs)")
st.plotly_chart(fig3, use_container_width=True)

buf3 = BytesIO()
fig3.write_image(buf3, format="png")
st.download_button("⬇️ Download Delivery Delay Chart", buf3.getvalue(), "delivery_delay_chart.png")

# PDF Report Export
st.subheader("📄 Export Full Report (PDF)")

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(200, 10, "Lakehouse360 Report", ln=True, align="C")

    def section_title(self, title):
        self.set_font("Arial", "B", 11)
        self.cell(200, 8, title, ln=True, align="L")

    def section_text(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, text)

if st.button("📤 Generate PDF Report"):
    pdf = PDF()
    pdf.add_page()
    pdf.section_title("Top Products by Revenue")
    for _, row in revenue_df.iterrows():
        pdf.section_text(f"{row['product_name']}: ${row['revenue']:.2f}")

    pdf.section_title("Most Returned Products")
    for _, row in returns_df.iterrows():
        pdf.section_text(f"{row['product_name']}: {row['num_returns']} returns")

    pdf.section_title("Delivery Delay by Courier")
    for _, row in delay_df.iterrows():
        pdf.section_text(f"{row['courier']}: {row['delay_hours']:.2f} hrs delay")

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    st.download_button("📥 Download PDF Report", data=pdf_output.getvalue(), file_name="lakehouse_report.pdf", mime="application/pdf")

# Auto-refresh every 5 minutes
st.markdown("""
<script>
    setTimeout(() => window.location.reload(), 300000);
</script>
""", unsafe_allow_html=True)
