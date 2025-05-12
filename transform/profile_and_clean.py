
import duckdb

# Connect to existing DB
con = duckdb.connect("duckdb/lakehouse.duckdb")

# List of tables to analyze
tables = [
    "customers", "orders", "inventory", "deliveries",
    "feedback", "suppliers", "products", "returns", "employees"
]

print("🔍 Profiling Summary")
print("=" * 50)

for table in tables:
    print(f"\n📊 Table: {table}")
    
    # Total row count
    row_count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"Total rows: {row_count}")
    
    # Get column names
    cols = con.execute(f"PRAGMA table_info('{table}')").fetchdf()["name"].tolist()
    
    # Null analysis per column
    print("Null values per column:")
    for col in cols:
        null_count = con.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL").fetchone()[0]
        if null_count > 0:
            print(f"  ⚠️  {col}: {null_count} nulls")
    print("✅ Null scan complete.")

    # Duplicate check based on likely key
    pk_col = f"{table[:-1]}_id" if table != "inventory" else "product_id"
    try:
        duplicates = con.execute(f'''
            SELECT {pk_col}, COUNT(*) AS dupes
            FROM {table}
            GROUP BY {pk_col}
            HAVING COUNT(*) > 1
            LIMIT 5;
        ''').fetchdf()
        if not duplicates.empty:
            print(f"⚠️  Duplicate {pk_col} values:")
            print(duplicates)
        else:
            print(f"✅ No duplicates in {pk_col}")
    except Exception as e:
        print(f"⚠️  Skipped duplicate check for {table}: {str(e)}")

con.close()
print("\n🧼 Ready to start cleaning in the next step.")
