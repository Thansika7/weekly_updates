import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime

fake = Faker('en_IN')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

NUM_CUSTOMERS = 300
NUM_ORDERS = 350

products = ["Laptop","Mobile","Tablet","Headphones","Camera","Dress","Shoes","Watch","Bag","Sunglasses","Sofa","Dining Table","Bed","Bookshelf","TV","Refrigerator"]
categories = ["Electronics","Electronics","Electronics","Accessories","Electronics","Apparel","Footwear","Jewelry","Accessories","Eyewear","Furniture","Furniture","Furniture","Furniture","Electronics","Appliances"]

stores = ["Chennai","Bangalore","Hyderabad","Delhi","Mumbai"]
payments = ["Cash","Card","UPI"]

customers = []
orders = []

today = datetime.today().strftime('%Y%m%d')

fake.unique.clear()

for i in range(NUM_CUSTOMERS):

    customers.append({
        "name": fake.name(),
        "email": fake.unique.email(),
        "gender": random.choice(["Male","Female"]),
        "age": random.randint(18,60),
        "city": fake.city()
    })


for order_num in range(1, NUM_ORDERS + 1):

    customer_ref = random.randint(1, NUM_CUSTOMERS)

    num_products = random.randint(1,3)

    for _ in range(num_products):

        product = random.choice(products)

        orders.append({
            "order_num": order_num,
            "customer_ref": customer_ref,
            "product": product,
            "category": categories[products.index(product)],
            "quantity": random.randint(1,5),
            "amount": random.randint(500,5000),
            "store_location": random.choice(stores),
            "date": datetime.today().strftime('%Y-%m-%d'),
            "payment_method": random.choice(payments)
        })


customers_df = pd.DataFrame(customers)
orders_df = pd.DataFrame(orders)

customers_df.to_csv(f"{OUTPUT_FOLDER}/customer_details_{today}.csv", index=False)
orders_df.to_csv(f"{OUTPUT_FOLDER}/order_details_{today}.csv", index=False)

print("Daily CSV files generated successfully")