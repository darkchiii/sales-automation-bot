import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import date
import os
from dotenv import load_dotenv


scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

load_dotenv()
spreadheet_key = os.getenv('SPREADSHEET_KEY')
sheet = client.open_by_key().sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)
# print(data[:5])


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

def validate_data():
    for column, rules in RULES.items():
        if rules["type"] in [int, float]:
            df[column] = pd.to_numeric(df[column], errors="coerce")
        elif rules["type"] == "date":
            df[column] = pd.to_datetime(df[column], errors="coerce")

    all_errors = []


    for i, row in df.iterrows():
        errors = []
        for column, rules in RULES.items():
            print(f"{i+1} iteracja:")
            # print(row[column])
            # print(rules["required"])

            if rules["required"] and pd.isnull(row[column]):
                errors.append(f"{column}: Error cell empty")

            if rules["type"] in [int, float]:
                if not pd.api.types.is_numeric_dtype(type(row[column])):
                    errors.append(f"{column}: Error data type")


            if "min" in rules and not pd.isnull(row[column]) and row[column] < rules["min"]:
                errors.append(f"{column}: Value error")

        print(f"Row {i} errors: {errors}")
        all_errors.append("; ".join(errors))
    df["error_flags"] = all_errors

