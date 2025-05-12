
import pandas as pd
import numpy as np
import random
import uuid
import json
import os
from faker import Faker
import pyarrow as pa
import pyarrow.parquet as pq

fake = Faker()
Faker.seed(200)
random.seed(200)

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Generate products.parquet
def generate_products(n=10000):
    records = []
    categories = ["Electronics", "Clothing", "Books", "Beauty", "Groceries"]
    for _ in range(n):
        records.append({
            "product_id": str(uuid.uuid4()),
            "product_name": fake.word().capitalize(),
            "category": random.choice(categories),
            "brand": fake.company(),
            "weight_grams": round(random.uniform(100, 5000), 2),
            "price": round(random.uniform(5, 1000), 2),
            "currency": "AUD",
            "release_date": fake.date_between(start_date='-5y', end_date='today').isoformat(),
            "discontinued": random.choice([True, False]),
            "rating": round(random.uniform(1, 5), 2),
            "num_reviews": random.randint(0, 5000)
        })
    df = pd.DataFrame(records)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, f"{output_dir}/products.parquet")

# Generate suppliers.tsv
def generate_suppliers(n=1000):
    records = []
    for _ in range(n):
        records.append({
            "supplier_id": str(uuid.uuid4()),
            "supplier_name": fake.company(),
            "contact_name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "country": fake.country(),
            "rating": random.choice(["A", "B", "C", "D"]),
            "active": random.choice(["Yes", "No", "yes", "no", "Y", "N"]),
            "established_year": random.randint(1990, 2023),
            "num_products_supplied": random.randint(5, 100)
        })
    df = pd.DataFrame(records)
    df.to_csv(f"{output_dir}/suppliers.tsv", sep='\t', index=False)

# Generate employees.csv
def generate_employees(n=1000):
    records = []
    roles = ["Warehouse Manager", "Delivery Driver", "Data Entry", "Support Staff", "Inventory Analyst"]
    for _ in range(n):
        records.append({
            "employee_id": str(uuid.uuid4()),
            "full_name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "hire_date": fake.date_between(start_date='-10y', end_date='today').isoformat(),
            "role": random.choice(roles),
            "shift": random.choice(["Morning", "Evening", "Night"]),
            "salary": round(random.uniform(40000, 120000), 2),
            "is_active": random.choice(["True", "False", "true", "false", "1", "0"]),
            "supervisor": fake.name()
        })
    df = pd.DataFrame(records)
    df.to_csv(f"{output_dir}/employees.csv", index=False)

# Generate returns.jsonl
def generate_returns(n=5000):
    with open(f"{output_dir}/returns.jsonl", "w") as f:
        for _ in range(n):
            record = {
                "return_id": str(uuid.uuid4()),
                "order_id": str(uuid.uuid4()),
                "reason": random.choice(["Damaged", "Wrong item", "Late delivery", "Other"]),
                "refund_amount": round(random.uniform(10, 500), 2),
                "currency": "AUD",
                "return_date": fake.date_between(start_date='-6m', end_date='today').isoformat(),
                "processed_by": fake.name(),
                "status": random.choice(["Pending", "Approved", "Rejected"]),
                "notes": random.choice(["", fake.sentence(), fake.sentence()])
            }
            f.write(json.dumps(record) + "\n")

if __name__ == "__main__":
    generate_products()
    generate_suppliers()
    generate_employees()
    generate_returns()
    print("✅ Additional datasets generated: products.parquet, suppliers.tsv, employees.csv, returns.jsonl")
