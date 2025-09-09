import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
from dotenv import load_dotenv
from config import Config

# Connect with Google Sheets

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
load_dotenv()


def load_data():
    try:
        spreadheet_key = Config.SPREADSHEET_KEY

        if not spreadheet_key:
            raise ValueError("SPREADSHEET_KEY not found in environment variables.")


        sheet = client.open_by_key(spreadheet_key).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("No data in spreadsheet.")

        return df, sheet
    except Exception as e:
        print(f"Error while loading data: {e}")
        raise
