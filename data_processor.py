import pandas as pd
from datetime import date, datetime, timedelta

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

def validate_data(df):
    df_copy = df.copy()
    df_copy["Date"] = pd.to_datetime(df_copy["Date"])

    for column, rules in RULES.items():
        if rules["type"] in [int, float]:
            df_copy[column] = pd.to_numeric(df_copy[column], errors="coerce")
        elif rules["type"] == "date":
            df_copy[column] = pd.to_datetime(df_copy[column], errors="coerce")

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
                if not pd.api.types.is_numeric_dtype(type(row[column])):
                    errors.append(f"{column}: Error data type")

            if "min" in rules and not pd.isnull(row[column]) and row[column] < rules["min"]:
                errors.append(f"{column}: Value error")

        # print(f"Row {i} errors: {errors}")
        all_errors.append("; ".join(errors))
    df_copy["error_flags"] = all_errors

    errors_only = [err for err in all_errors if err]
    df_copy = df_copy.fillna("")

    return df_copy, errors_only

def update_total_cost_column(df):
    df["Total cost"] = df["Quantity"] * df["Price"]

    # df = df.fillna("")
    if pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

def save_to_sheets(df, sheet):
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
