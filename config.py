import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SPREADSHEET_KEY = os.getenv('SPREADSHEET_KEY')

    CHART_WIDTH = 800
    CHART_HEIGHT = 500

    DEFAULT_TREND_DAYS = 30
    DEFAULT_DAILY_DAYS = 7