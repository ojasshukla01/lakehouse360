
import duckdb
import os

# Create output folder for DuckDB database
os.makedirs("duckdb", exist_ok=True)

# Connect to local DuckDB instance
con = duckdb.connect("duckdb/lakehouse.duckdb")

# Load CSVs
con.execute("""
CREATE OR REPLACE TABLE customers AS
SELECT * FROM read_csv_auto('data/customers.csv');
""")

con.execute("""
CREATE OR REPLACE TABLE orders AS
SELECT * FROM read_csv_auto('data/orders.csv');
""")

con.execute("""
CREATE OR REPLACE TABLE inventory AS
SELECT * FROM read_csv_auto('data/inventory.csv');
""")

con.execute("""
CREATE OR REPLACE TABLE deliveries AS
SELECT * FROM read_csv_auto('data/deliveries.csv');
""")

# Load JSONL
con.execute("""
CREATE OR REPLACE TABLE feedback AS
SELECT * FROM read_json_auto('data/feedback.jsonl', format='newline_delimited');
""")

# Load TSV
con.execute("""
CREATE OR REPLACE TABLE suppliers AS
SELECT * FROM read_csv_auto('data/suppliers.tsv', delim='\t');
""")

# Load Parquet
con.execute("""
CREATE OR REPLACE TABLE products AS
SELECT * FROM read_parquet('data/products.parquet');
""")

# Load JSONL (returns)
con.execute("""
CREATE OR REPLACE TABLE returns AS
SELECT * FROM read_json_auto('data/returns.jsonl', format='newline_delimited');
""")

# Load CSV
con.execute("""
CREATE OR REPLACE TABLE employees AS
SELECT * FROM read_csv_auto('data/employees.csv');
""")

# Verify counts
tables = [
    "customers", "orders", "inventory", "deliveries",
    "feedback", "suppliers", "products", "returns", "employees"
]
for table in tables:
    count = con.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
    print(f"✅ Loaded {table}: {count} rows")

# Preview schema for customers
print("\n📌 Sample Schema for 'customers':")
print(con.execute("DESCRIBE customers;").fetchdf())

con.close()
