# Sales Analytics & Automation Bot

A comprehensive sales analytics system with Google Sheets integration, data validation, and automated Telegram bot reporting. This project was created to enhance skills with numpy, pandas, work with large datasets, and develop commercial Telegram bots for clients.

## Why I made this project?

This project was developed to:

* **Deepen expertise** with numpy, pandas, and large dataset manipulation
* **Develop analytical system skills** for real-world applications
* **Prepare for commercial projects** - Telegram bots for business clients
* **Master external API integration** (Google Sheets, Telegram)
* **Build automated reporting systems** for business intelligence

## Current Features

### Sales Analytics

* **Daily reports** - day-by-day sales analysis
* **Trend analysis** - flexible time periods (last N days or date ranges)
* **Top products** - ranking by quantity, orders, and revenue
* **Best customers** - activity and value analysis with engagement metrics

### Data Validation & Processing

* **Automatic validation** of all records against business rules
* **Error detection** - empty fields, invalid data types, out-of-range values
* **Error flagging** - written directly to Google Sheets for tracking
* **Automatic calculations** - total order costs and derived metrics

### Data Visualization

* **Interactive charts** using Plotly with professional styling
* **Flexible parameters** - customizable titles, date ranges, and chart types
* **Data export** - ready for further processing and analysis

## Still working on

* Telegram bot integration with commands for trends, orders, and reports
* Sending charts, tables, and formatted reports directly in Telegram
* Secure user authentication for bot access
* Automated scheduling of daily reports (e.g., at 9:00 AM)
* Multi-channel delivery to users, groups, and channels
* Smart notifications and alerts for anomalies or trends
* Automated file attachments (charts, CSV exports)

## Tech Stack

* **Python 3.9+** - Core language
* **Pandas** - Data analysis and manipulation
* **NumPy** - Numerical computations
* **Plotly** - Interactive data visualizations
* **Google Sheets API** - Spreadsheet integration
* **gspread** - Simplified Google Sheets handling
* **python-dotenv** - Environment variable management
* **APScheduler** *(planned)* - Task scheduling
* **python-telegram-bot** *(planned)* - Telegram integration

##  Dependencies

Dependencies are managed with **uv** and fully tracked in `uv.lock`. Key packages include:

* **pandas** - Data analysis and manipulation
* **numpy** - Numerical computations
* **plotly** - Interactive visualizations
* **gspread** - Google Sheets integration
* **google-auth** - Google API authentication
* **python-dotenv** - Environment variables

## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/darkchiii/sales-automation-bot.git
cd sales-automation-bot
```

2. **Install uv (if not already installed):**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

3. **Install dependencies with uv:**

```bash
uv sync
```

4. **Google Sheets API setup:**

   * Create a project in [Google Cloud Console](https://console.cloud.google.com)
   * Enable Google Sheets API and Google Drive API
   * Create a Service Account and download the JSON key
   * Save the key as `credentials.json` in the root directory

5. **Environment configuration:**

```bash
# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

`.env` file structure:

```env
SPREADSHEET_KEY=your_google_sheets_key
TELEGRAM_BOT_TOKEN=your_bot_token  # (planned)
CHAT_ID=your_chat_id              # (planned)
```

## Usage

### Basic execution

```bash
python main.py
```

### Module import

```python
from data_loader import load_data
from analytics import get_daily_sales, products_performance, top_customers

# Load data
df, sheet = load_data()

# Daily sales analysis
daily_sales = get_daily_sales(df)

# Product performance
top_products = products_performance(df, time_period=30)

# Customer analysis
best_customers = top_customers(df)
```

### Data validation

```python
from data_processor import validate_data, update_total_cost_column

# Validate and clean data
clean_df, errors = validate_data(df)
if errors:
    print(f"Found {len(errors)} validation errors")

# Update calculated fields
update_total_cost_column(clean_df)
```

## Project Structure

```
sales-automation-bot/
├──  data/                    # Sample data files
│   └── orders_demo.csv         # Demo dataset
├──  analytics.py             # Sales analysis functions
├──  config.py                # Configuration management
├──  data_loader.py           # Google Sheets integration
├──  data_processor.py        # Data validation & processing
├──  main.py                  # Main execution script
├──  reports.py               # Report generation (planned)
├──  requirements.txt         # Python dependencies
├──  .env.example             # Environment template
├──  README.md                # Project documentation
└──  credentials.json         # Google API credentials (excluded)
```

##  Configuration

### Chart settings (`config.py`)

```python
class Config:
    CHART_WIDTH = 800
    CHART_HEIGHT = 500
    DEFAULT_TREND_DAYS = 30
    DEFAULT_DAILY_DAYS = 7
```

### Data validation rules (`data_processor.py`)

* **OrderID**: Required integer, minimum value 1
* **Product**: Required string
* **Quantity**: Required integer, minimum value 1
* **Price**: Required number, minimum value 0
* **Date**: Required valid date format

##  Available Analytics

### Daily Sales Report

```python
daily_sales = get_daily_sales(df)
# Returns: Date-indexed series with daily totals
```

### Sales Trend Analysis

```python
# Last 30 days
trend = sales_analysis(df, time_period=30)

# Specific date range
trend = sales_analysis(df, start_date="2025-08-01", end_date="2025-08-31")
```

### Product Performance

```python
products = products_performance(df, time_period=30)
# Returns: DataFrame with total_quantity, num_orders, total_revenue
```

### Customer Analysis

```python
customers = top_customers(df)
# Returns: DataFrame with num_orders, orders_cost, days_since_last_order
```
