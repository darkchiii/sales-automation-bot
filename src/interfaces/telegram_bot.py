from datetime import datetime, timedelta
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler
from src.utils.config import Config

from src.core.data_loader import load_data
from src.core.data_processor import validate_data, update_total_cost_column
from src.core.analytics import sales_analysis, products_performance

import plotly.express as px
import io

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def daily_sales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df, sheet = load_data()
    clean_df, errors = validate_data(df)
    daily = sales_analysis(clean_df, time_period=7)
    daily_sum =daily["Total cost"].sum()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"\nTotal sales:\n{daily_sum} \nDaily sales: {daily} ")

async def trend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("How to use: /trend <number of days>")
            return
        days = int(context.args[0])

        df, sheet = load_data()
        clean_df, errors = validate_data(df)
        sales_daily = sales_analysis(clean_df, time_period=days)

        sales_daily["Date"] = sales_daily["Date"].dt.strftime("%Y-%m-%d")

        fig = px.line(sales_daily, x="Date", y="Total cost", title=f"Sales trend {days} days")
        img_bytes = io.BytesIO()
        fig.write_image(img_bytes, format="png")
        img_bytes.seek(0)
        await update.message.reply_photo(photo=img_bytes)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def top_products(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_to_message("How to use: /top_products <number_of_days>")
        return
    days = int(context.args[0])

    df, sheet = load_data()
    clean_df, errors = validate_data(df)
    top_products = products_performance(clean_df, days)

    top_products_reset = top_products.reset_index()
    msg = f"Top products from {days} days:\n"
    for i, row in top_products_reset.iterrows():
        msg += f"{row['Product']}: quantity={row['total_quantity']}, orders={row['num_orders']}, revenue={row['total_revenue']}\n"
    await update.message.reply_text(msg)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).build()

    # Listening to /start command
    start_handler = CommandHandler('start', start)
    daily_sales_handler = CommandHandler('daily_sales', daily_sales)
    trend_handler = CommandHandler('trend', trend)
    top_products_handler = CommandHandler('top_products', top_products)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(daily_sales_handler)
    application.add_handler(trend_handler)
    application.add_handler(top_products_handler)
    application.add_handler(unknown_handler)

    application.run_polling()


