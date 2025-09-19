import pandas as pd
from datetime import date, datetime, timedelta
import numpy as np
import json

RULES = {
    "OrderID": {
        "required": True,
        "type": int,
        "min": 1
    },
    "Product": {
        "required": True,
        "type": str,
    },
    "Quantity": {
        "required": True,
        "type": int,
        "min": 1
    },
    "Price": {
        "required": True,
        "type": (int, float),
        "min": 0
    },
    "Date": {
        "required": True,
        "type": date
    }
}

def string_to_datetime(df):
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

def datetime_to_string(df):
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")


def validate_data(df):
    try:
        if df is None:
            raise ValueError("There is no DataFrame to validate")
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Pandas DataFrame expected, got {type(df)}")
        if df.empty:
            raise ValueError("DataFrame is empty")

        required_columns = list(RULES.keys())
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")

        df_copy = df.copy()
        string_to_datetime(df_copy)

        for column, rules in RULES.items():

            if rules["type"] in [int, float]:
                df_copy[column] = pd.to_numeric(df_copy[column], errors="coerce")

        all_errors = []

        for i, row in df_copy.iterrows():
            errors = []
            for column, rules in RULES.items():
            # print(f"{i+1} iteracja:")
            # print(row[column])
            # print(rules["required"])

                if rules["required"] and pd.isnull(row[column]):
                    errors.append(f"{column}: Error cell empty")

                if rules["type"] in [int, float]:
                    if not pd.api.types.is_numeric_dtype(df_copy[column]):
                        errors.append(f"{column}: Error data type")

                if "min" in rules and not pd.isnull(row[column]) and row[column] < rules["min"]:
                    errors.append(f"{column}: Value error")

        # print(f"Row {i} errors: {errors}")
            all_errors.append("; ".join(errors))
        df_copy["error_flags"] = all_errors

        errors_only = [err for err in all_errors if err]

        for col in df_copy.columns:
            if df_copy[col].dtype == 'object':
                df_copy[col] = df_copy[col].fillna("")

        return df_copy, errors_only
    except Exception as e:
        raise ValueError(f"Error: {e}")

def update_total_cost_column(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Pandas DataFrame expected, got {type(df)}")
    if df.empty:
        raise ValueError("DataFrame is empty")

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Total cost"] = df["Quantity"] * df["Price"]

    # df = df.fillna("")
    if pd.api.types.is_datetime64_any_dtype(df["Date"]):
        datetime_to_string(df)

def save_to_sheets(df, sheet):

    # print("Typy kolumn:")
    # print(df.dtypes)
    # print("\nPierwszy wiersz:")
    # print(df.iloc[0])
    # print("\nTypy wartości pierwszego wiersza:")
    # for col in df.columns:
    #     print(f"{col}: {type(df.iloc[0][col])}")

    try:
        if pd.api.types.is_datetime64_any_dtype(df["Date"]):
            datetime_to_string(df)
        df = df.replace([np.nan, pd.NaT], None)

        test_data = [df.columns.values.tolist()] + df.values.tolist()
        json.dumps(test_data)  # Jeśli przejdzie, to OK
        sheet.update(test_data)

    except json.JSONEncodeError as e:
        print(f"JSON serialization error: {e}")

    except Exception as e:
        print(f"Error: {e}")
        raise

