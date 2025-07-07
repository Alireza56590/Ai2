import os
import logging
import asyncio
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = os.environ.get("TELEGRAM_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route('/')
def home():
    logging.info("✅ Health check OK")
    return "Bot is alive!"

async def start(update, context):
    logging.info(f"📩 Received /start from {update.effective_user.id}")
    await update.message.reply_text("✅ Bot is alive and working!")

async def run_bot():
    try:
        logging.info("🚀 Starting polling with ApplicationBuilder")
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        await application.run_polling()
    except Exception as e:
        logging.error(f"❌ Exception in run_bot: {e}")

if __name__ == "__main__":
    logging.info("🔧 Main starting")
    def poll():
        try:
            asyncio.run(run_bot())
        except Exception as e:
            logging.error(f"❌ Exception in polling thread: {e}")

    threading.Thread(target=poll).start()
    app.run(host="0.0.0.0", port=PORT)
