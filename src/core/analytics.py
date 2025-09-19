import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import date, datetime, timedelta
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import plotly.express as px

# for tests purpose
from src.core.data_loader import load_data
from src.core.data_processor import validate_data

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
    df_copy["Date"] = pd.to_datetime(df_copy["Date"])

    if time_period is not None and (start_date is not None or end_date is not None):
        raise ValueError("You can check the time period or results from a specific date to a specific date, not all at once.")
    if time_period is not None and time_period < 0:
        raise ValueError("Time period can't be negative value.")
    if start_date and end_date and start_date > end_date:
        raise ValueError("Start date must be earlier than end date.")

    if time_period:
        # time_period = 30
        start_date = datetime.now() - timedelta(time_period)
        filtered_data = df_copy[df_copy["Date"] >= start_date]
        # Check if filtered data has rows
        if filtered_data.empty:
            raise ValueError("There is no data to show in chosen time period")

        total_cost = filtered_data["Total cost"].sum()
        sales_daily = filtered_data.groupby("Date")["Total cost"].sum().reset_index()
        return sales_daily, total_cost

    elif start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        filtered_data = df_copy[(df_copy["Date"] >= start_date) & (df_copy["Date"] <= end_date)]
        if filtered_data.empty:
            raise ValueError("There is no data to show in chosen time period")

        sales_daily = filtered_data.groupby("Date")["Total cost"].sum().reset_index()
        total_cost = filtered_data["Total cost"].sum()

        return sales_daily, total_cost
    else:
        raise ValueError("You must provide either time_period OR start_date and end_date.")


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

if __name__ == "__main__":
    # Test data

    import pandas as pd
    # today = datetime.now().date()

    # test_data = {
    #     'Date': [today, today - timedelta(1), today - timedelta(2)] * 2,
    #     'Total cost': [100, 200, 150, 50, 75, 25]
    # }
    # df = pd.DataFrame(test_data)

    # daily, total = sales_analysis(df, time_period=7)
    # print(f"Total sum: {total}")
    # print(f"Daily breakdown:")
    # print(daily)
    # print(f"Daily as dict: {daily.to_dict()}")
    df, sheet = load_data()
    # clean_df, errors_list = validate_data(df)
    # df_copy = clean_df.copy()

    # daily, sum=sales_analysis(clean_df, time_period=1)
    # print(f"Total sum: {sum} \nDaily sales: {daily}")