import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.core.data_loader import load_data
from src.core.analytics import get_daily_sales, sales_analysis, products_performance, top_customers
from src.core.data_processor import validate_data, update_total_cost_column, save_to_sheets
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from datetime import date


def main():
    df, sheet = load_data()
    clean_df, errors_list = validate_data(df)

    if errors_list:
        st.write("Data loaded succesfully!")
        st.write(f"Errors spotted!: {errors_list}")

        add_radio = st.sidebar.radio(
            'Do you want me to write error flags to Sheets?',
            ('Yes', 'No'),
            index=1
        )
        if add_radio == "Yes":
            save_to_sheets(clean_df, sheet)

    add_radio2 = st.sidebar.radio(
        'Do you want me to write total order costs to Sheets?',
        ('Yes', 'No'),
        index=1
        )

    if add_radio2 == "Yes":
        update_total_cost_column(clean_df)
        save_to_sheets(clean_df, sheet)

    if st.checkbox('Show data:'):
        chart_data = clean_df
        st.dataframe(chart_data)

    option_analysis = st.selectbox(
        "Now we can start analyzing. What would you want to see?", # Pokazywać dopiero po przygptpwaniu danych?
        ("---", "Daily sales", "Sales analysis", "Top products", "Top customers")
        )

    if option_analysis == "Daily sales":
        st.dataframe(get_daily_sales(df))

    elif option_analysis == "Sales analysis":
        option_time = st.selectbox("What period of time are you interested in?",
                            ('---', 'Last X days', "From X date to Y date"),
        )
        if option_time == 'Last X days':
            days=st.number_input("Days", min_value=1, max_value=365, value=7, step=1)
            daily, total_cost = sales_analysis(clean_df, time_period=days)

            if daily.empty:
                st.warning("No sales in this period")
            else:
                st.write(f"Cost of orders: {total_cost}")
                st.dataframe(daily)

        if option_time == "From X date to Y date":
            start_date = st.date_input("Start date", date.today())
            end_date = st.date_input("End date", date.today())
            daily, total_cost = sales_analysis(clean_df, start_date=start_date, end_date=end_date)

            if daily.empty:
                st.warning("No sales in this period")
            else:
                st.write(f"Cost of orders: {total_cost}")
                st.dataframe(daily)

    elif option_analysis == "Top products":
        option_time = st.selectbox("What period of time are you interested in?",
                            ('---', 'Last X days', "From X date to Y date"),
        )
        if option_time == 'Last X days':
            days=st.number_input("Days", min_value=1, max_value=365, value=7, step=1)
            top_products = products_performance(clean_df, time_period=days)
            st.dataframe(top_products)
        if option_time == "From X date to Y date":
            start_date = st.date_input("Start date", date.today())
            end_date = st.date_input("End date", date.today())
            top_products = products_performance(clean_df, start_date=start_date, end_date=end_date)
            st.dataframe(top_products)
    elif option_analysis == "Top customers":
        filtered_customers = top_customers(clean_df)
        st.dataframe(filtered_customers)
