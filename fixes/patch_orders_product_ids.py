import json
import random
from pathlib import Path

DATA_DIR = Path("data/json_files")
ORDERS_PATH = DATA_DIR / "orders.json"
PRODUCTS_PATH = DATA_DIR / "products.json"

# Load valid product IDs
with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
    products = json.load(f)
    valid_product_ids = [p["product_id"] for p in products if "product_id" in p]

if not valid_product_ids:
    raise ValueError("No valid product IDs found in products.json")

# Patch orders
with open(ORDERS_PATH, "r", encoding="utf-8") as f:
    orders = json.load(f)

for order in orders:
    order["product_id"] = random.choice(valid_product_ids)

# Save back updated orders
with open(ORDERS_PATH, "w", encoding="utf-8") as f:
    json.dump(orders, f, indent=2)

print(f"✅ Patched {len(orders)} orders with valid product_id values.")
