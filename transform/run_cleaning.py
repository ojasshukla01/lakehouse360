
import duckdb

# Connect to DuckDB
con = duckdb.connect("duckdb/lakehouse.duckdb")

# Load and execute SQL script
with open("transform/clean_data.sql", "r") as f:
    sql = f.read()
    con.execute(sql)

con.close()
print("✅ Cleaning script executed. Cleaned tables created.")
