import os
import json
import duckdb
import pandas as pd
from pathlib import Path

# Paths
JSON_DIR = Path("data/json_files")
PARQUET_DIR = Path("output/cleaned_parquet")
PARQUET_DIR.mkdir(parents=True, exist_ok=True)

# UUID fields per table
UUID_COLUMNS = {
    "customers": ["customer_id"],
    "orders": ["order_id", "customer_id", "product_id"],
    "inventory": ["product_id", "supplier_id"],
    "deliveries": ["delivery_id", "order_id"],
    "feedback": ["supplier_id"],
    "suppliers": ["supplier_id"],
    "products": ["product_id"],
    "returns": ["return_id", "order_id"],
    "employees": ["employee_id"]
}

# DuckDB connection
con = duckdb.connect()

def cast_uuid_columns(df, uuid_cols):
    for col in uuid_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

def clean_table(table_name: str):
    try:
        # Load JSON
        json_path = JSON_DIR / f"{table_name}.json"
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)

        # Cast UUID columns to string
        df = cast_uuid_columns(df, UUID_COLUMNS.get(table_name, []))

        # Register for DuckDB SQL
        con.register(table_name, df)

        # Transformations
        if table_name == "customers":
            df_clean = con.execute(f"""
                SELECT 
                    customer_id,
                    TRIM(first_name) || ' ' || TRIM(last_name) AS name,
                    LOWER(email) AS email,
                    phone_number,
                    CAST(date_of_birth AS DATE) AS dob,
                    state, country, is_active
                FROM {table_name}
                WHERE customer_id IS NOT NULL
            """).df()

        elif table_name == "orders":
            df_clean = con.execute(f"""
                SELECT 
                    order_id, customer_id, product_id, product_name,
                    quantity, price_per_unit, currency,
                    status, payment_method, order_timestamp
                FROM {table_name}
                WHERE order_id IS NOT NULL AND product_id IS NOT NULL
            """).df()

        elif table_name == "inventory":
            df_clean = con.execute(f"""
                SELECT 
                    product_id, product_name, warehouse_id, stock_level, restock_date
                FROM {table_name}
                WHERE product_id IS NOT NULL
            """).df()

        elif table_name == "deliveries":
            df_clean = con.execute(f"""
                SELECT 
                    delivery_id, order_id, courier,
                    delivery_status, estimated_arrival, delivered_at
                FROM {table_name}
                WHERE order_id IS NOT NULL
            """).df()

        elif table_name == "feedback":
            df_clean = con.execute(f"""
                SELECT 
                    supplier_id, supplier_name, feedback_score, submitted_at
                FROM {table_name}
                WHERE supplier_id IS NOT NULL
            """).df()

        elif table_name == "suppliers":
            df_clean = con.execute(f"""
                SELECT 
                    supplier_id, supplier_name, country,
                    num_products_supplied
                FROM {table_name}
                WHERE supplier_id IS NOT NULL
            """).df()

        elif table_name == "products":
            df_clean = con.execute(f"""
                SELECT 
                    product_id, product_name, price, rating
                FROM {table_name}
                WHERE product_id IS NOT NULL AND price > 0
            """).df()

        elif table_name == "returns":
            df_clean = con.execute(f"""
                SELECT 
                    return_id, order_id, reason, refund_amount, return_date
                FROM {table_name}
                WHERE order_id IS NOT NULL
            """).df()

        elif table_name == "employees":
            df_clean = con.execute(f"""
                SELECT 
                    employee_id, full_name, role, salary
                FROM {table_name}
                WHERE employee_id IS NOT NULL
            """).df()

        else:
            print(f"❌ No rules defined for {table_name}")
            return

        # Save cleaned Parquet
        out_path = PARQUET_DIR / f"{table_name}.parquet"
        df_clean.to_parquet(out_path, index=False)
        print(f"✅ Cleaned & saved {table_name} -> {out_path.name}")

    except Exception as e:
        print(f"⚠️ Failed to clean {table_name}.json: {e}")

if __name__ == "__main__":
    for table in UUID_COLUMNS:
        clean_table(table)
