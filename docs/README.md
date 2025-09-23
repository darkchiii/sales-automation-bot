# Sales Analytics & Automation Bot

A comprehensive sales analytics system with Google Sheets integration, data validation and automated reporting capabilities. The system provides three different interfaces: command-line interface, web application with Streamlit, and Telegram bot for automated reporting.

## Overview

This project was developed to deepen expertise with data analysis libraries, build real-world analytical systems and create commercial-grade automation solutions for business intelligence.

## Features

### Core Analytics Engine
- **Daily Sales Reports**: Comprehensive day-by-day sales analysis with trend visualization
- **Time-Period Analysis**: Flexible reporting for last N days or custom date ranges
- **Product Performance**: Ranking by quantity sold, order count, and total revenue
- **Customer Analytics**: Activity tracking with purchase history

### Data Processing & Validation
- **Automatic Data Validation**: Business rule enforcement with error detection
- **Data Quality Assurance**: Empty field detection, type validation, and range checking
- **Error Reporting**: Direct error flagging written to Google Sheets for tracking
- **Calculated Fields**: Automatic total cost computation and derived metrics

### Multi-Interface Access

#### 1. Command Line Interface (CLI)
- Interactive data analysis through terminal
- Direct Google Sheets integration
- Real-time data validation and processing
- Batch operations for data cleanup

#### 2. Web Application (Streamlit)
- User-friendly web interface
- Interactive data visualization
- Real-time chart generation
- Configurable analysis parameters
- Link: https://sales-analysis-automation.streamlit.app/

#### 3. Telegram Bot Integration
- Automated daily reports via Telegram
- On-demand trend analysis with `/trend` command
- Top products reporting with `/top_products`
- Interactive chart delivery directly in chat

## Technical Stack

### Core Technologies
- **Python 3.9+**: Primary development language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Plotly**: Interactive data visualizations

### Integration & APIs
- **Google Sheets API**: Spreadsheet data source integration
- **gspread**: Simplified Google Sheets handling
- **python-telegram-bot**: Telegram automation
- **Streamlit**: Web application framework

### Development Tools
- **uv**: Modern Python package management
- **python-dotenv**: Environment configuration management
- **matplotlib**: Additional plotting capabilities

## Installation

### Prerequisites
- Python 3.9 or higher
- Google Cloud Platform account for Sheets API
- Telegram Bot Token (for bot functionality)

### Setup Process

1. **Clone Repository**
```bash
git clone https://github.com/darkchiii/sales-automation-bot.git
cd sales-analytics-automation-bot
```

2. **Install Dependencies**
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

3. **Google Sheets API Configuration**
   - Create project in [Google Cloud Console](https://console.cloud.google.com)
   - Enable Google Sheets API and Google Drive API
   - Create Service Account and download JSON credentials
   - Save credentials as `credentials.json` in project root

4. **Environment Configuration**
```bash
# Create environment file
cp .env.example .env
```

Configure `.env` file:
```env
SPREADSHEET_KEY=your_google_sheets_document_key
TELEGRAM_TOKEN=your_telegram_bot_token
```

## Usage

### Command Line Interface
```bash
python -m src.interfaces.cli
```

Interactive CLI provides:
- Data loading and validation
- Error reporting and correction
- Analytics generation
- Direct Google Sheets updates

### Web Application

Link: https://sales-analysis-automation.streamlit.app/

![Image of Visualization App 1](https://github.com/darkchiii/sales-automation-bot/blob/main/data/screenshots/1.png)

![Image of Visualization App 1](https://github.com/darkchiii/sales-automation-bot/blob/main/data/screenshots/2.png)

Web interface features:
- Interactive data exploration
- Visual analytics dashboard
- Configurable reporting parameters
- Real-time chart generation

### Telegram Bot
```bash
python -m src.interfaces.telegram_bot
```

Available bot commands:
- `/start` - Initialize bot interaction
- `/daily_sales` - Get recent daily sales summary
- `/trend <days>` - Generate sales trend chart for specified period
- `/top_products <days>` - List top-performing products

## Project Structure

```
sales-analytics-automation-bot/
├── data/                       # Sample datasets
│   └── orders_demo.csv           # Demo sales data
├── docs/                       # Documentation
│   └── README.md                 # Project documentation
├── src/                        # Source code
│   ├── core/                     # Core business logic
│   │   ├── analytics.py            # Sales analysis functions
│   │   ├── data_loader.py          # Google Sheets integration
│   │   └── data_processor.py       # Data validation & processing
│   ├── interfaces/               # User interfaces
│   │   ├── cli.py                  # Command-line interface
│   │   ├── telegram_bot.py         # Telegram bot implementation
│   │   └── web_app.py              # Streamlit web application
│   └── utils/                    # Utilities and configuration
│       └── config.py               # Configuration management
├── streamlit_app.py            # Streamlit application entry point
├── credentials.json            # Google API credentials (excluded from git)
├── pyproject.toml              # Project configuration
└── uv.lock                     # Dependency lock file
```

## Data Validation Rules

The system enforces comprehensive data validation:

- **OrderID**: Required integer, minimum value 1
- **CustomerName**: Required string field
- **Product**: Required product name
- **Quantity**: Required integer, minimum value 1
- **Price**: Required numeric value, minimum value 0
- **Date**: Required valid date format

## Available Analytics

### Daily Sales Analysis
```python
daily_sales = get_daily_sales(df)
# Returns: Date-indexed series with daily revenue totals
```

### Trend Analysis
```python
# Last 30 days trend
trend_data, total = sales_analysis(df, time_period=30)

# Custom date range
trend_data, total = sales_analysis(df, start_date="2025-08-01", end_date="2025-08-31")
```

### Product Performance
```python
products = products_performance(df, time_period=30)
# Returns: DataFrame with total_quantity, num_orders, total_revenue
```

### Customer Intelligence
```python
customers = top_customers(df)
# Returns: DataFrame with num_orders, orders_cost, days_since_last_order
```

## Configuration

### Chart Settings
Configurable visualization parameters in `src/utils/config.py`:
```python
CHART_WIDTH = 800
CHART_HEIGHT = 500
DEFAULT_TREND_DAYS = 30
DEFAULT_DAILY_DAYS = 7
```

## Development Status

### Current Features
- Complete data validation and processing pipeline
- Google Sheets integration with error reporting
- Three fully functional interfaces (CLI, Web, Telegram)
- Interactive data visualizations
- Flexible time-period analysis

### Future Enhancements
- Automated report scheduling
- Advanced anomaly detection
- Enhanced security features
- Performance optimization for large datasets