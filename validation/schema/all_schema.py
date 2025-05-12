from pydantic import BaseModel
from typing import Optional
from datetime import date

class Customer(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postcode: Optional[str]
    country: Optional[str]
    signup_date: Optional[date]
    loyalty_score: Optional[float]
    preferred_store: Optional[str]
    is_active: Optional[bool]

class Order(BaseModel):
    order_id: str
    customer_id: str
    order_date: date
    order_status: str
    payment_method: str
    total_amount: float
    shipped_date: Optional[date]

class InventoryItem(BaseModel):
    product_id: str
    quantity_available: int
    restock_date: Optional[date]

class Delivery(BaseModel):
    delivery_id: str
    order_id: str
    delivered_at: Optional[date]
    delivery_status: str
    estimated_arrival: Optional[date]

class Feedback(BaseModel):
    feedback_text: str
    feedback_score: Optional[float]
    submitted_at: Optional[date]
    supplier_id: str

class Supplier(BaseModel):
    supplier_id: str
    supplier_name: str
    contact_name: str
    contact_email: str
    phone_number: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postcode: Optional[str]
    country: Optional[str]

class Product(BaseModel):
    product_id: str
    product_name: str
    category: str
    price: float
    supplier_id: str
    stock_quantity: int

class Return(BaseModel):
    return_id: str
    order_id: str
    return_date: Optional[date]
    return_reason: Optional[str]
    refunded_amount: Optional[float]

class Employee(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    role: str
    email: str
    phone_number: Optional[str]
    hire_date: Optional[date]
    department: Optional[str]
