"""Send telegram message to a telegram group"""
import os
import logging
import sys

import requests
from dotenv import load_dotenv


def get_telegram_creds():
    """Load Telegram API token and channel ID"""
    load_dotenv()
    logging.info("Reading telegram data from .env")
    telegram_api = os.getenv("TELEGRAMAPI")
    telegram_channel_id = os.getenv("TELEGRAMCHANNELID")
    if telegram_api is None or telegram_channel_id is None:
        logging.error("Either telegram api or telegram channel id in .env is null")
        sys.exit()

    return telegram_api, telegram_channel_id


def send_telegram_image(filename):
    """Send a message to telegram in a specific group"""
    telegram_api, telegram_channel_id = get_telegram_creds()
    openfile = open(filename, "rb")

    logging.info("Send message to telegram bot")
    url = (
        f"https://api.telegram.org/bot{telegram_api}/sendPhoto?chat_id="
        f"{telegram_channel_id}"
    )
    response = requests.post(url=url, files={"photo": openfile}, timeout=15)
    if response.status_code != 200:
        logging.error("Error while posting to telegram API %s", response.status_code)
        print("Error while posting to telegram API %s", response.status_code)


def send_telegram_message(message):
    """Send a message to telegram in a specific group"""
    telegram_api, telegram_channel_id = get_telegram_creds()

    logging.info("Send message to telegram bot")
    url = (
        f"https://api.telegram.org/bot{telegram_api}/sendMessage?chat_id="
        f"{telegram_channel_id}&text={message}"
    )
    response = requests.post(url=url, timeout=15)
    if response.status_code != 200:
        logging.error("Error while posting to telegram API %s", response.status_code)
        print("Error while posting to telegram API %s", response.status_code)
