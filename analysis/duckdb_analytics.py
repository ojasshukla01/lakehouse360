from pathlib import Path
import duckdb

# Define path to cleaned parquet files
cleaned_data_path = Path("output/cleaned_parquet")

# DuckDB in-memory connection
con = duckdb.connect(database=":memory:")

# Tables to register
tables = [
    "customers", "orders", "inventory", "deliveries", "feedback",
    "suppliers", "products", "returns", "employees"
]

# Register tables
for table in tables:
    file_path = cleaned_data_path / f"{table}.parquet"
    try:
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM read_parquet('{file_path.as_posix()}')")
        print(f"✅ Registered: {table}")
    except Exception as e:
        print(f"⚠️ Failed to register {table}: {e}")

# Basic record counts
print("\n📊 Table Record Counts:")
for table in ["customers", "orders", "products", "returns", "deliveries"]:
    try:
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count} rows")
    except Exception as e:
        print(f"{table}: Error - {e}")

# Sample key values
print("\n🔍 Sample ID Previews:")
try:
    print("customers.customer_id:", con.execute("SELECT customer_id FROM customers LIMIT 3").fetchall())
    print("orders.customer_id:", con.execute("SELECT customer_id FROM orders LIMIT 3").fetchall())
    print("products.product_id:", con.execute("SELECT product_id FROM products LIMIT 3").fetchall())
    print("orders.product_id:", con.execute("SELECT product_id FROM orders LIMIT 3").fetchall())
except Exception as e:
    print("⚠️ Error previewing keys:", e)

# Check join matches
print("\n🔍 Orders with unknown product_id:")
print(con.execute("""
    SELECT o.product_id 
    FROM orders o
    LEFT JOIN products p ON o.product_id = p.product_id
    WHERE p.product_id IS NULL
    LIMIT 10
""").fetchdf())

# 1. Top 5 Products by Revenue
print("\n📊 Top 5 Products by Revenue")
try:
    df = con.execute("""
        SELECT 
            p.product_name,
            SUM(o.quantity * o.price_per_unit) AS total_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """).df()
    print(df)
except Exception as e:
    print(f"⚠️ Revenue query failed: {e}")

# 2. Most Returned Products
print("\n📦 Most Returned Products")
try:
    df = con.execute("""
        SELECT 
            p.product_name,
            COUNT(*) AS num_returns
        FROM returns r
        JOIN orders o ON r.order_id = o.order_id
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY num_returns DESC
        LIMIT 5
    """).df()
    print(df)
except Exception as e:
    print(f"⚠️ Returns query failed: {e}")

# 3. Top Customers by Orders
print("\n🧑‍🤝‍🧑 Top 5 Customers by Orders")
try:
    df = con.execute("""
        SELECT 
            name,
            COUNT(*) AS total_orders
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY name
        ORDER BY total_orders DESC
        LIMIT 5
    """).df()
    print(df)
except Exception as e:
    print(f"⚠️ Customers query failed: {e}")

# 4. Average Delivery Time by Courier
print("\n🚚 Average Delivery Time by Courier")
try:
    df = con.execute("""
        SELECT 
            d.courier,
            ROUND(AVG(EXTRACT(EPOCH FROM (CAST(d.delivered_at AS TIMESTAMP) - CAST(o.order_timestamp AS TIMESTAMP))) / 3600.0), 2) AS avg_delivery_hours
        FROM deliveries d
        JOIN orders o ON d.order_id = o.order_id
        WHERE d.delivered_at IS NOT NULL AND o.order_timestamp IS NOT NULL
        GROUP BY d.courier
        ORDER BY avg_delivery_hours
    """).df()
    print(df)
except Exception as e:
    print(f"⚠️ Delivery time query failed: {e}")
