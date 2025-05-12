import os
import json
from pathlib import Path
from pydantic import ValidationError
from validation.schema.all_schema import (
    Customer, Order, InventoryItem, Delivery, Feedback,
    Supplier, Product, Return, Employee
)

# Map of table name to schema class
SCHEMA_MAP = {
    "customers": Customer,
    "orders": Order,
    "inventory": InventoryItem,
    "deliveries": Delivery,
    "feedback": Feedback,
    "suppliers": Supplier,
    "products": Product,
    "returns": Return,
    "employees": Employee,
}

DATA_FOLDER = Path("data/json_files")
VALIDATED_FOLDER = Path("validation/validated")
LOGS_FOLDER = Path("validation/logs")
VALIDATED_FOLDER.mkdir(parents=True, exist_ok=True)
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)

def validate_table(table_name: str):
    schema = SCHEMA_MAP[table_name]
    file_path = DATA_FOLDER / f"{table_name}.json"

    if not file_path.exists():
        print(f"❌ Failed to read {table_name}: No file found at {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    valid_rows, errors = [], []

    for idx, record in enumerate(data):
        try:
            validated = schema(**record)
            valid_rows.append(validated.model_dump())
        except ValidationError as ve:
            errors.append({
                "index": idx,
                "errors": ve.errors(),
                "record": record
            })

    with open(VALIDATED_FOLDER / f"{table_name}.json", "w", encoding="utf-8") as f:
        json.dump(valid_rows, f, indent=2)

    if errors:
        with open(LOGS_FOLDER / f"{table_name}_errors.json", "w", encoding="utf-8") as f:
            json.dump(errors, f, indent=2)
        print(f"⚠️  {table_name}: {len(errors)} invalid rows logged.")
    else:
        print(f"✅ {table_name}: All records are valid.")

if __name__ == "__main__":
    for table in SCHEMA_MAP:
        validate_table(table)
