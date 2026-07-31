import pandas as pd
import streamlit as st


@st.cache_data
def load_data():

    # Load CSV files
    customers = pd.read_csv("Data/customers.csv")
    order_items = pd.read_csv("Data/order_items (1).csv")
    orders = pd.read_csv("Data/orders (1).csv")
    products = pd.read_csv("Data/products (1).csv")

    # Convert date columns
    customers["signup_date"] = pd.to_datetime(customers["signup_date"])
    orders["order_date"] = pd.to_datetime(orders["order_date"])

    # Merge all tables
    df_master = (
        order_items
        .merge(orders, on="order_id", how="inner")
        .merge(customers, on="customer_id", how="inner")
        .merge(products, on="product_id", how="inner")
    )

    # Calculate line revenue
    df_master["line_revenue"] = (
        df_master["quantity"]
        * df_master["unit_price"]
        * (1 - df_master["discount"])
    )

    # Create order month
    df_master["order_month"] = (
        df_master["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    # Separate cancelled and active orders
    cancelled_orders = df_master[
        df_master["order_status"] == "Cancelled"
    ]

    active_orders = df_master[
        df_master["order_status"] != "Cancelled"
    ]

    return df_master, active_orders, cancelled_orders