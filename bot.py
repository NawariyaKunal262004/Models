from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import psutil

Bot_Token = ""

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    message = (
        f"CPU Usage: {cpu}%\n"
        f"RAM Usage: {mem.percent}%\n"
        f"Disk Usage: {disk.percent}%"
    )

    await update.message.reply_text(message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I can monitor system status. Use /status to check CPU, RAM, and Disk usage.")

if _name_ == "_main_":
    app = ApplicationBuilder().token(Bot_Token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    print("Bot is running...")
    app.run_polling()