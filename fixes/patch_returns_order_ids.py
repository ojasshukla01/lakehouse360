import json
import random
from pathlib import Path

DATA_DIR = Path("data/json_files")
RETURNS_PATH = DATA_DIR / "returns.json"
ORDERS_PATH = DATA_DIR / "orders.json"

# Load valid order IDs
with open(ORDERS_PATH, "r", encoding="utf-8") as f:
    orders = json.load(f)
    valid_order_ids = [o["order_id"] for o in orders if "order_id" in o]

if not valid_order_ids:
    raise ValueError("No valid order IDs found.")

# Patch returns
with open(RETURNS_PATH, "r", encoding="utf-8") as f:
    returns = json.load(f)

for r in returns:
    r["order_id"] = random.choice(valid_order_ids)

with open(RETURNS_PATH, "w", encoding="utf-8") as f:
    json.dump(returns, f, indent=2)

print(f"✅ Patched {len(returns)} returns with valid order_id values.")
