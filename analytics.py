import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import date, datetime, timedelta
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import plotly.express as px

def generate_diagram(title, data):
    fig = px.line(data, x=data.index, y="Total cost", title=f"title")
    fig.show()
    return fig

# Daily sales raport
def get_daily_sales(df):
    daily_sales = df.groupby("Date")["Total cost"].sum()

    if input("Do you want to generate diagram? (y/n): ") == 'y':
        title = input("Title: ").strip()
        if not title:
            title="Daily sales report"
        generate_diagram(title=title, data=daily_sales)
    return daily_sales

# Sales analysis; define time period in days or start and end date of time you are interested in
def sales_analysis(df, time_period=None, start_date=None, end_date=None):
    df_copy = df.copy()
    if time_period is not None and (start_date is not None or end_date is not None):
        raise ValueError("Podaj albo time_period, albo start_date i end_date, nie oba naraz")
    df_copy["Date"] = pd.to_datetime(df_copy["Date"])

    if time_period:
        # time_period = 30
        start_date = datetime.now() - timedelta(time_period)
        sales = df_copy[df_copy["Date"] >= start_date].groupby("Date")["Total cost"].sum()
        return sales
    elif start_date and end_date:
        sales = df_copy[(df_copy["Date"] >= start_date) & (df_copy["Date"] <= end_date)].groupby("Date")["Total cost"].sum()
        return sales

# Product performance analysis; define time period in days or start and end date of time you are interested in
def products_performance(df, time_period=None, start_date=None, end_date=None):
    df_copy = df.copy()
    df_copy["Date"] = pd.to_datetime(df_copy["Date"])

    if time_period and (start_date or end_date):
        raise ValueError("Podaj albo time_period, albo start_date i end_date, nie oba naraz")

    if time_period:
        # time_period = 30
        start_date = datetime.now() - timedelta(time_period)
        products_within_dates = df_copy[df_copy["Date"] >= start_date]
    elif start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        products_within_dates = df_copy[(df_copy["Date"] >= start_date) & (df_copy["Date"] <= end_date)]
    else:
        products_within_dates = df_copy

    top_products = products_within_dates.groupby("Product").agg(
        total_quantity=("Quantity", "sum"),
        num_orders=("OrderID", "count"),
        total_revenue=("Total cost", "sum")
    )
    top_products = top_products.sort_values(by="total_quantity", ascending=False)
    return top_products

# Top customers analysis
def top_customers(df):
    df_copy = df.copy()
    df_copy["Date"] = pd.to_datetime(df_copy["Date"])

    top_customers = df_copy.groupby("CustomerName").agg(
        num_orders = ("OrderID", "count"),
        orders_cost = ("Total cost", "sum"),
        last_order = ("Date", "max")
    )

    top_customers["days_since_last_order"] = (datetime.now() - pd.to_datetime(top_customers["last_order"])).dt.days
    top_customers = top_customers.drop(columns="last_order").sort_values(by="num_orders", ascending=False)

    return top_customers

