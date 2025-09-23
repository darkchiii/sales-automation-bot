import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.config import Config

# Connect with Google Sheets
scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

def load_data():
    try:
        load_dotenv()
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        print("Credentials loaded")
        client = gspread.authorize(creds)
        print("Client authorized")
        try:
            spreadheet_key = Config.SPREADSHEET_KEY
        except AttributeError:
            raise ValueError("Spreadsheet key not defined in file: config.py. Please set SPREADSHEET_KEY.")

        if not spreadheet_key:
            raise ValueError("SPREADSHEET_KEY is empty. Please set it in environment variables or config.py.")
        sheet = client.open_by_key(spreadheet_key).sheet1
        print("Spreadsheet opened")
        data = sheet.get_all_records()
        print(f"Got {len(data)} records")
        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("No data in spreadsheet.")

        return df, sheet
    except FileNotFoundError as e:
        print(f"Credentials file - credentials.json not found: {e}")
        raise
    except Exception as e:
        print(f"Error while loading data: {e}")
        raise


def load_data_web():
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scopes
        )
        client = gspread.authorize(creds)
        try:
            spreadsheet_key = st.secrets["gcp_service_account"]["SPREADSHEET_KEY"]
        except AttributeError:
            raise ValueError("Spreadsheet key not defined. Please set SPREADSHEET_KEY.")

        if not spreadsheet_key:
            raise ValueError("SPREADSHEET_KEY is empty.")
        sheet = client.open_by_key(spreadsheet_key).sheet1

        print("Spreadsheet opened")
        data = sheet.get_all_records()
        print(f"Got {len(data)} records")
        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("No data in spreadsheet.")

        return df, sheet
    except FileNotFoundError as e:
        print(f"Credentials file - credentials.json not found: {e}")
        raise
    except Exception as e:
        print(f"Error while loading data: {e}")
        raise