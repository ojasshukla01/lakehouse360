import json
import random
from pathlib import Path

DATA_DIR = Path("data/json_files")
ORDERS_PATH = DATA_DIR / "orders.json"
CUSTOMERS_PATH = DATA_DIR / "customers.json"

# Load valid customer IDs
with open(CUSTOMERS_PATH, "r", encoding="utf-8") as f:
    customers = json.load(f)
    valid_customer_ids = [c["customer_id"] for c in customers if "customer_id" in c]

if not valid_customer_ids:
    raise ValueError("No valid customer IDs found.")

# Patch orders
with open(ORDERS_PATH, "r", encoding="utf-8") as f:
    orders = json.load(f)

for order in orders:
    order["customer_id"] = random.choice(valid_customer_ids)

with open(ORDERS_PATH, "w", encoding="utf-8") as f:
    json.dump(orders, f, indent=2)

print(f"✅ Patched {len(orders)} orders with valid customer_id values.")
