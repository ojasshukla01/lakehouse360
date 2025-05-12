
import pandas as pd
from faker import Faker
import random
import uuid
import json
import os

# Setup
fake = Faker()
Faker.seed(100)
random.seed(100)

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Generate Customers
def generate_customers(n=50000):
    data = []
    for _ in range(n):
        profile = fake.simple_profile()
        data.append({
            "customer_id": str(uuid.uuid4()),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": profile["mail"],
            "phone_number": fake.phone_number(),
            "date_of_birth": profile["birthdate"],
            "gender": profile["sex"],
            "address": fake.address().replace("\n", ", "),
            "city": fake.city(),
            "state": fake.state(),
            "postcode": fake.postcode(),
            "country": fake.country(),
            "signup_date": fake.date_between(start_date='-3y', end_date='today'),
            "loyalty_score": round(random.uniform(0, 100), 2),
            "preferred_store": random.choice(["Online", "In-store", "Mobile App"]),
            "is_active": random.choice([True, False])
        })
    df = pd.DataFrame(data)
    df.to_csv(f"{output_dir}/customers.csv", index=False)

# Generate Orders
def generate_orders(n=50000):
    records = []
    for _ in range(n):
        records.append({
            "order_id": str(uuid.uuid4()),
            "customer_id": str(uuid.uuid4()),
            "product_id": str(uuid.uuid4()),
            "product_name": fake.word().capitalize(),
            "quantity": random.randint(1, 10),
            "price_per_unit": round(random.uniform(5.0, 200.0), 2),
            "currency": "AUD",
            "payment_method": random.choice(["Credit Card", "PayPal", "Afterpay", "Bank Transfer"]),
            "order_timestamp": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
            "status": random.choice(["Shipped", "Delivered", "Returned", "Cancelled"])
        })
    df = pd.DataFrame(records)
    df.to_csv(f"{output_dir}/orders.csv", index=False)

# Generate Inventory
def generate_inventory(n=10000):
    records = []
    for _ in range(n):
        records.append({
            "product_id": str(uuid.uuid4()),
            "product_name": fake.word().capitalize(),
            "stock_level": random.randint(0, 500),
            "warehouse_id": fake.bothify(text='WH###'),
            "supplier_id": str(uuid.uuid4()),
            "restock_date": fake.date_between(start_date='-6m', end_date='+3m').isoformat(),
            "expiry_date": fake.date_between(start_date='+3m', end_date='+2y').isoformat()
        })
    df = pd.DataFrame(records)
    df.to_csv(f"{output_dir}/inventory.csv", index=False)

# Generate Deliveries
def generate_deliveries(n=30000):
    records = []
    for _ in range(n):
        records.append({
            "delivery_id": str(uuid.uuid4()),
            "order_id": str(uuid.uuid4()),
            "courier": random.choice(["AusPost", "Toll", "DHL", "FedEx"]),
            "delivery_status": random.choice(["Scheduled", "Out for Delivery", "Delivered", "Failed"]),
            "estimated_arrival": fake.future_datetime(end_date="+15d").isoformat(),
            "delivered_at": fake.date_time_between(start_date='-3d', end_date='now').isoformat(),
            "route": fake.city() + " → " + fake.city()
        })
    df = pd.DataFrame(records)
    df.to_csv(f"{output_dir}/deliveries.csv", index=False)

# Generate Feedback
def generate_feedback(n=10000):
    feedback = []
    for _ in range(n):
        feedback.append({
            "supplier_id": str(uuid.uuid4()),
            "supplier_name": fake.company(),
            "feedback_score": random.randint(1, 5),
            "feedback_text": fake.sentence(nb_words=10),
            "submitted_at": fake.date_time_this_year().isoformat()
        })
    with open(f"{output_dir}/feedback.json", "w") as f:
        json.dump(feedback, f, indent=2)

# Main
if __name__ == "__main__":
    generate_customers()
    generate_orders()
    generate_inventory()
    generate_deliveries()
    generate_feedback()
    print("✅ All synthetic data files generated in ./data/")
