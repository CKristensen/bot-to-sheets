from datetime import date
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from loguru import logger
from jobs.domain import AllergySymptoms, HealthStatus, FastingHours
from jobs.repo import GoogleSheets
from oauth2client.service_account import ServiceAccountCredentials
from typing import TypeVar

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json",
    [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ],
)


def connect_to_sheets() -> GoogleSheets:
    with open(".googlesheets.key") as f:
        key = f.readline().strip()
    sheets = GoogleSheets(key, creds)
    return sheets


help_text = """
/help -> Receive help message.
/health -> register your overall health status from 1 to 10. 1 being almost dead and 10 being awesome.
/allergy -> register your overall allergy status from 1 to 10. 1 being no allergies and 10 being incapacitated.
/fasting -> register number of hours your last fast was.
"""


def get_token():
    with open(".telegram.key") as f:
        token = f.readline().replace("\n", "")
    return token


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE, entry_type):
    try:
        logger.info(update.message.text)
        status = update.message.text.split(" ")[-1]
        status = int(status)
        assert entry_type.validate(status)
        conn = connect_to_sheets()
        conn.set(entry_type(date=date.today(), level=status))
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=entry_type.success_message(len(conn.get_all())),
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=entry_type.error_message(),
        )


def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return status(update, context, HealthStatus)


def allergy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return status(update, context, AllergySymptoms)


def fasting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return status(update, context, FastingHours)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


if __name__ == "__main__":
    logger.info("starting")
    application = ApplicationBuilder().token(get_token()).build()
    logger.info("application set up!")

    help_handler = CommandHandler("help", help)
    health_handler = CommandHandler("health", health)
    fasting_hours_handler = CommandHandler("fasting", health)
    allergy_handler = CommandHandler("allergy", allergy)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(help_handler)
    application.add_handler(health_handler)
    application.add_handler(allergy_handler)
    application.add_handler(fasting_hours_handler)
    application.add_handler(echo_handler)

    logger.info("application run!")
    application.run_polling()
