import logging
import logging.config
import os
from typing import List
from dotenv import load_dotenv
from src.TooGoodToGoNotifier.tooGoodToGoClient import TooGoodToGoClient
from src.TooGoodToGoNotifier.notifierSender import EmailNotifier


def setUpLogger():
    logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
    return logging.getLogger(__name__)

def run():
    env_path = 'D:\\Szymon\\programming\\python\\TooGoodToGoNotifier\\.env'
    load_dotenv(env_path)
    logger = setUpLogger()
    latitude = float(os.getenv("latitude".upper()))
    longitude = float(os.getenv("longitude".upper()))
    radius = int(os.getenv("radius".upper()))
    credentials_path = os.getenv("credentials_path".upper())
    tgtgClient = TooGoodToGoClient(latitude, longitude, radius, credentials_path)
    notifier = EmailNotifier([os.getenv("RECEIVER_EMAIL"), ], env_path)

    available_orders = tgtgClient.getAvailableToOrder()
    if available_orders:
        notifier.notify("Avaible order in your place.")
    else:
        logger.info("No avaible order in your place.")

if __name__ == '__main__':
    run()
