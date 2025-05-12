import json
import random
from pathlib import Path

DATA_DIR = Path("data/json_files")
ORDERS_PATH = DATA_DIR / "orders.json"
DELIVERIES_PATH = DATA_DIR / "deliveries.json"

# Load valid order IDs
with open(ORDERS_PATH, "r", encoding="utf-8") as f:
    orders = json.load(f)
    valid_order_ids = [o["order_id"] for o in orders if "order_id" in o]

# Load and patch deliveries
with open(DELIVERIES_PATH, "r", encoding="utf-8") as f:
    deliveries = json.load(f)

for d in deliveries:
    d["order_id"] = random.choice(valid_order_ids)

with open(DELIVERIES_PATH, "w", encoding="utf-8") as f:
    json.dump(deliveries, f, indent=2)

print(f"✅ Patched {len(deliveries)} deliveries with valid order_id values.")
