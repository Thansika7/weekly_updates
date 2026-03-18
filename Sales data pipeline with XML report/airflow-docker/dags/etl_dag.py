from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import mysql.connector
import os
import json
import xml.etree.ElementTree as ET
from lxml import etree

UPLOAD_PATH = "/opt/airflow/uploads/"
TMP_PATH = "/tmp/etl/"
os.makedirs(TMP_PATH, exist_ok=True)

def extract():
    customer_file = max(
        [f for f in os.listdir(UPLOAD_PATH) if f.startswith("customer_details")]
    )
    order_file = max(
        [f for f in os.listdir(UPLOAD_PATH) if f.startswith("order_details")]
    )

    customers = pd.read_csv(os.path.join(UPLOAD_PATH, customer_file))
    orders = pd.read_csv(os.path.join(UPLOAD_PATH, order_file))

    customers.dropna(subset=["email"], inplace=True)
    orders.dropna(subset=["customer_ref","product","store_location"], inplace=True)

    customers.to_csv(TMP_PATH + "customers.csv", index=False)
    orders.to_csv(TMP_PATH + "orders.csv", index=False)
    print("Latest files extracted successfully")

def transform():
    customers = pd.read_csv(TMP_PATH + "customers.csv")
    orders = pd.read_csv(TMP_PATH + "orders.csv")

    customers.fillna({"name":"Unknown","city":"Unknown","gender":"Unknown","age":0}, inplace=True)
    orders.fillna({"product":"Unknown","category":"Unknown","quantity":0,"amount":0,"store_location":"Unknown","payment_method":"Unknown"}, inplace=True)

    customers.drop_duplicates(subset=["email"], inplace=True)
    orders.drop_duplicates(subset=["order_num","product","store_location"], inplace=True)

    customers["customer_id"] = customers.index + 1

    orders["customer_ref"] = orders["customer_ref"].astype(int)
    customers["customer_id"] = customers["customer_id"].astype(int)

    fact_sales = orders.merge(customers, left_on="customer_ref", right_on="customer_id", how="inner")

    dim_customer = customers[["name","email","gender","age","city"]].drop_duplicates()
    dim_product = orders[["product","category"]].drop_duplicates()
    dim_store = orders[["store_location"]].drop_duplicates()

    fact_sales["profit"] = fact_sales["quantity"] * fact_sales["amount"]
    total_profit = fact_sales["profit"].sum() if not fact_sales.empty else 0

    if not fact_sales.empty and not fact_sales["product"].dropna().empty:
        most_sold_product = fact_sales.groupby("product")["quantity"].sum().idxmax()
    else:
        most_sold_product = "N/A"

    if not fact_sales.empty and not fact_sales["store_location"].dropna().empty:
        top_store = fact_sales.groupby("store_location")["profit"].sum().idxmax()
    else:
        top_store = "N/A"

    kpi = {"profit": float(total_profit), "product": most_sold_product, "store": top_store}

    dim_customer.to_csv(TMP_PATH + "dim_customer.csv", index=False)
    dim_product.to_csv(TMP_PATH + "dim_product.csv", index=False)
    dim_store.to_csv(TMP_PATH + "dim_store.csv", index=False)
    fact_sales.to_csv(TMP_PATH + "fact_sales.csv", index=False)

    with open(TMP_PATH + "kpi.json","w") as f:
        json.dump(kpi,f)

def load():

    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="sales_etl"
    )

    cursor = conn.cursor()

    dim_customer = pd.read_csv(TMP_PATH + "dim_customer.csv")
    dim_product = pd.read_csv(TMP_PATH + "dim_product.csv")
    dim_store = pd.read_csv(TMP_PATH + "dim_store.csv")
    fact_sales = pd.read_csv(TMP_PATH + "fact_sales.csv")

    for _, r in dim_customer.iterrows():
        cursor.execute("""
            INSERT INTO dim_customer (name,email,gender,age,city)
            VALUES (%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), city=VALUES(city)
        """, (r["name"], r["email"], r["gender"], r["age"], r["city"]))

    for _, r in dim_product.iterrows():
        cursor.execute("""
            INSERT INTO dim_product (product,category)
            VALUES (%s,%s)
            ON DUPLICATE KEY UPDATE category=VALUES(category)
        """, (r["product"], r["category"]))

    for _, r in dim_store.iterrows():
        cursor.execute("""
            INSERT INTO dim_store (store_location)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE store_location=VALUES(store_location)
        """, (r["store_location"],))


    with open(TMP_PATH + "kpi.json") as f:
        kpi = json.load(f)

    cursor.execute("""
        INSERT INTO dim_analytics (total_profit, most_sold_product, top_store)
        VALUES (%s,%s,%s)
    """, (kpi["profit"], kpi["product"], kpi["store"]))

    cursor.execute("SELECT LAST_INSERT_ID()")
    analytics_id = cursor.fetchone()[0]


    for _, r in fact_sales.iterrows():

        email = str(r["email"]).strip()
        product = str(r["product"]).strip()
        category = str(r["category"]).strip()
        store_location = str(r["store_location"]).strip()

        cursor.execute("SELECT customer_id FROM dim_customer WHERE email=%s", (email,))
        customer_id = cursor.fetchone()[0]

        cursor.execute("SELECT product_id FROM dim_product WHERE product=%s AND category=%s", (product, category))
        product_id = cursor.fetchone()[0]

        cursor.execute("SELECT store_id FROM dim_store WHERE store_location=%s", (store_location,))
        store_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT IGNORE INTO fact_sales
            (order_num, customer_id, product_id, store_id, quantity, amount, payment_method, date, profit, analytics_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            r["order_num"],
            customer_id,
            product_id,
            store_id,
            r["quantity"],
            r["amount"],
            r["payment_method"],
            r["date"],
            r["profit"],
            analytics_id
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Load completed successfully")

def export_xml():
    conn = mysql.connector.connect(host="mysql", user="root", password="root", database="sales_etl")
    query = """
    SELECT 
        f.order_num,
        f.quantity,
        f.amount,
        f.payment_method,
        f.date,

        c.name AS customer_name,
        c.email AS customer_email,
        c.city AS customer_city,

        p.product,
        p.category,

        s.store_location,

        a.total_profit,
        a.most_sold_product,
        a.top_store

    FROM fact_sales f

    LEFT JOIN dim_customer c 
    ON f.customer_id = c.customer_id

    LEFT JOIN dim_product p 
    ON f.product_id = p.product_id

    LEFT JOIN dim_store s 
    ON f.store_id = s.store_id

    LEFT JOIN dim_analytics a
    ON f.analytics_id = a.analytics_id
    """
    df = pd.read_sql(query, conn)

    root = ET.Element("Sales")

    for order_id, group in df.groupby("order_num"):
        order = ET.SubElement(root, "Order")
        ET.SubElement(order, "OrderID").text = str(order_id)
        ET.SubElement(order, "OrderDate").text = str(group.iloc[0]["date"])

        customer = ET.SubElement(order, "Customer")
        ET.SubElement(customer, "Name").text = str(group.iloc[0]["customer_name"])
        ET.SubElement(customer, "Email").text = str(group.iloc[0]["customer_email"])
        ET.SubElement(customer, "City").text = str(group.iloc[0]["customer_city"])

        store = ET.SubElement(order, "Store")
        ET.SubElement(store, "Location").text = str(group.iloc[0]["store_location"])

        ET.SubElement(order, "PaymentMethod").text = str(group.iloc[0]["payment_method"])

        items = ET.SubElement(order, "Items")
        for _, row in group.iterrows():
            item = ET.SubElement(items, "Item")
            ET.SubElement(item, "Product").text = str(row["product"])
            ET.SubElement(item, "Category").text = str(row["category"])
            ET.SubElement(item, "Quantity").text = str(row["quantity"])
            ET.SubElement(item, "Amount").text = str(row["amount"])

        analytics = ET.SubElement(order, "Analytics")
        ET.SubElement(analytics, "TotalProfit").text = str(group.iloc[0]["total_profit"])
        ET.SubElement(analytics, "MostSoldProduct").text = str(group.iloc[0]["most_sold_product"])
        ET.SubElement(analytics, "TopStore").text = str(group.iloc[0]["top_store"])

    ET.indent(tree := ET.ElementTree(root), space="  ")
    tree.write(UPLOAD_PATH + "sales_source.xml", encoding="utf-8", xml_declaration=True)
    conn.close()
    print("XML exported successfully")
    
def transform_xml(xml_file, xslt_file, output_file):
    xml_path = os.path.join(UPLOAD_PATH, xml_file)
    xslt_path = os.path.join(UPLOAD_PATH, xslt_file)

    script_dir = os.path.dirname(__file__)
    output_folder = os.path.join(script_dir, "xml report")
    os.makedirs(output_folder, exist_ok=True) 
    output_path = os.path.join(output_folder, output_file)

    dom = etree.parse(xml_path)
    xslt = etree.parse(xslt_path)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)

    newdom.write(output_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    print(f"Transformed XML created: {output_path}")

def run_all_transform_xml():
    transform_xml("sales_source.xml", "customer.xslt", "customers_report.xml")
    transform_xml("sales_source.xml", "product.xslt", "products_report.xml")
    transform_xml("sales_source.xml", "analytics.xslt", "analytics_report.xml")

default_args = {"owner":"airflow", "start_date":datetime(2024,1,1)}

with DAG(dag_id="sales_etl_star_schema",
         default_args=default_args,
         schedule="@daily",
         catchup=True) as dag:

    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)
    t4 = PythonOperator(task_id="export_xml", python_callable=export_xml)
    t5 = PythonOperator(task_id="transform_xml", python_callable=run_all_transform_xml)

    t1 >> t2 >> t3 >> t4 >> t5