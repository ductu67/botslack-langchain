import logging

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    logger.info("CALL start")
    await update.message.reply_text(
        "Hello! You can type /help to learn how I can assist you."
    )


async def help_command(update: Update, context: CallbackContext):
    logger.info("CALL help")
    await update.message.reply_text(
        "/vn_express - I will send you one of the most read news articles from VNExpress.\n"
        "/bao_moi - I will send you one of the most read news articles from BaoMoi.\n\n"
        "/help - Shows this help message"
    )


async def bao_moi(update: Update, context: CallbackContext):
    logger.info("CALL bao_moi")
    logger.info("Sending request to https://baomoi.com/tin-moi.epi")

    s = requests.Session()
    response = s.get("https://baomoi.com/tin-moi.epi")
    soup = BeautifulSoup(response.content, 'html.parser')

    logger.info("Got response: %d", response.status_code)
    if response.status_code != 200:
        await update.message.reply_text("Oops! Something went wrong :(")
        return

    new_list = soup.find_all("h3", {"class": "font-semibold block"})
    if len(new_list) == 0:
        await update.message.reply_text("Oops! Something went wrong! Couldn't find any videos :(")
        return
    await update.message.reply_text("Latest News from BaoMoi")
    for index, new in zip(range(10), new_list):
        new = new.next
        await update.message.reply_text(new.attrs.get("title") + ": " + "https://baomoi.com/" + new.attrs.get("href"))


async def vn_express(update: Update, context: CallbackContext):
    logger.info("CALL vn_express")
    logger.info("Sending request to https://vnexpress.net/tin-tuc-24h")

    s = requests.Session()
    response = s.get("https://vnexpress.net/tin-tuc-24h")
    soup = BeautifulSoup(response.content, 'html.parser')

    logger.info("Got response: %d", response.status_code)
    if response.status_code != 200:
        await update.message.reply_text("Oops! Something went wrong :(")
        return

    new_list = soup.find_all("h3", {"class": "title-news"})
    if len(new_list) == 0:
        await update.message.reply_text("Oops! Something went wrong! Couldn't find any videos :(")
        return
    await update.message.reply_text("Latest News from VnExpress")
    for index, new in zip(range(10), new_list):
        new = new.text
        await update.message.reply_text(new)


def main():
    logger.info("CALL main")

    # Get token from environment variable
    TOKEN = "7026724431:AAG7BUkmn5__a0oL42xvIp0AzGLdrNITgcc"
    if not TOKEN:
        logger.error("Error: TELEGRAM_TOKEN environment variable is not set")
        return

    application = Application.builder().token(TOKEN).build()

    logger.info("Configuring handlers")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("vn_express", vn_express))
    application.add_handler(CommandHandler("bao_moi", bao_moi))

    logger.info("Starting the bot")
    application.run_polling()


if __name__ == "__main__":
    main()
