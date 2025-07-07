import os
import logging
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
        logging.info("🚀 Building application")
        application = ApplicationBuilder().token(TOKEN).build()
        
        logging.info("🔧 Adding handlers")
        application.add_handler(CommandHandler("start", start))
        
        logging.info("🔄 Starting polling")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        logging.info("🤖 Bot is now running")
        return application
        
    except Exception as e:
        logging.error(f"❌ Exception in run_bot: {e}")
        raise

def start_bot():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = loop.run_until_complete(run_bot())
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("🛑 Received stop signal, shutting down..")
    finally:
        loop.run_until_complete(bot.shutdown())
        loop.close()

if __name__ == "__main__":
    from threading import Thread
    
    logging.info("🔧 Starting bot thread")
    bot_thread = Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    logging.info("🌐 Starting Flask server")
    app.run(host="0.0.0.0", port=PORT, use_reloader=False)
