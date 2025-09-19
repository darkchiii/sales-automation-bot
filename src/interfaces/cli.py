from src.core.data_processor import validate_data, update_total_cost_column, save_to_sheets
from src.core.data_loader import load_data
from src.core.analytics import get_daily_sales, sales_analysis, products_performance, top_customers
import pandas as pd

def main():
    print("Loading data...")
    df, sheet = load_data()
    print(f"Success: {len(df)} rows loaded!")

    # Data validation
    clean_df, errors_list = validate_data(df)
    if errors_list:
        print(f"Errors: {errors_list[:5]}")
    else:
        print("No errors")

    print(f"Cleaned data: {len(clean_df)} rows")

    if input("Write error flags to Sheets? (y/n): ") == 'y':
        save_to_sheets(clean_df, sheet)

    if input("Write total order costs to Sheets? (y/n): ") == 'y':
        update_total_cost_column(clean_df)
        save_to_sheets(clean_df, sheet)
        print("Saved")

    print("\nData Analysis:")

    # Daily sales analysis
    daily_sales = get_daily_sales(clean_df)
    print("Daily Sales:")
    print(daily_sales.tail(7))

    # Sales analysis for the last 30 days
    sales_30_days = sales_analysis(clean_df, time_period=30)
    print("\nSales (last 30 days):")
    print(sales_30_days)

    #  Sales analysis for a selected period
    sales_period = sales_analysis(clean_df, start_date="2025-08-06", end_date="2025-08-15")
    print("\nSales (2025-08-06 to 2025-08-15):")
    print(sales_period)

    # Top products for all time
    top_products = products_performance(clean_df)
    #time_period=30
    # print("\nTop Products for last 30 days ")
    print(top_products.head())

    # # Top products for a selected period
    top_products = products_performance(clean_df, start_date="2025-08-06", end_date="2025-08-15")
    print("\nTop products (2025-08-06 to 2025-08-15):")

    # # Top customers
    best_customers = top_customers(clean_df)
    print("\nTop Customers:")
    print(best_customers.head())

    # Test
    # empty_df = pd.DataFrame()
    # validate_data(empty_df)

    # df_without_columns = pd.DataFrame({'WrongColumn': [1, 2, 3]})
    # validate_data(df_without_columns)
    # df = None
    # result = validate_data(df)
    # if result:
    #     clean_df, errors = result


if __name__ == "__main__":
    main()