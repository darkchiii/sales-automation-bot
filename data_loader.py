import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
from dotenv import load_dotenv

# Connect with Google Sheets

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
load_dotenv()


def load_data():
    spreadheet_key = os.getenv('SPREADSHEET_KEY')
    sheet = client.open_by_key(spreadheet_key).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df, sheet
