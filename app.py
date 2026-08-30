import os
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)

@app.get("/")
def home():
    return "Versace Exchange is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💰 Купить LTC"],
        ["📋 Мои заявки", "📈 Курс"],
        ["🆘 Поддержка"]
    ]

    await update.message.reply_text(
        "🟣 VERSACE EXCHANGE\n\n"
        "Добро пожаловать!\n\n"
        "💵 Курс: 1 USD = 20 MDL\n"
        "🪙 Покупка Litecoin (LTC)",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📈 Курс":
        await update.message.reply_text(
            "📈 Текущий курс Versace:\n\n"
            "1 USD = 20 MDL"
        )

    elif text == "💰 Купить LTC":
        await update.message.reply_text(
            "💰 Введите сумму в USD.\n\n"
            "Например: 100"
        )

    elif text == "📋 Мои заявки":
        await update.message.reply_text(
            "📋 У вас пока нет заявок."
        )

    elif text == "🆘 Поддержка":
        await update.message.reply_text(
            "🆘 Поддержка Versace\n\n"
            "Ожидайте ответа оператора."
        )

    else:
        try:
            usd = float(text.replace(",", "."))
            mdl = usd * 20

            await update.message.reply_text(
                f"💵 Вы хотите получить: {usd:.2f} USD в LTC\n\n"
                f"💰 К оплате: {mdl:.2f} MDL\n\n"
                "📈 Курс: 1 USD = 20 MDL\n\n"
                "⚠️ Это тестовый расчёт."
            )

        except ValueError:
            await update.message.reply_text(
                "Пожалуйста, введите сумму в USD, например:\n"
                "100"
            )

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

async def run_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    while True:
        await __import__("asyncio").sleep(3600)

def main():
    threading.Thread(target=run_flask, daemon=True).start()

    import asyncio
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
