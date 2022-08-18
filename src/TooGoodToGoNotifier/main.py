import logging
import logging.config
import os
from dotenv import load_dotenv

from src.TooGoodToGoNotifier.tooGoodToGoClient import TooGoodToGoClient, initTgtgClientFromEnv
from src.TooGoodToGoNotifier.notifierSender import EmailNotifier
from src.TooGoodToGoNotifier.utils import JsonDb, saveToJson


def setUpLogger():
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"

    logging.basicConfig(filename="logfile.log",
                        filemode="a",
                        format=Log_Format,
                        level=logging.INFO)

    return logging.getLogger(__name__)


def addIfNotExists(available_orders, db):
    """Returns True if any object was added."""

    anyNew = False
    for order in available_orders:
        pk = order["item"]["item_id"]
        added = db.addIfUnique(pk, order)
        if added:
            anyNew = True
    return anyNew





def run():
    env_path = 'D:\\Szymon\\programming\\python\\TooGoodToGoNotifier\\.env'
    load_dotenv(env_path)
    logger = setUpLogger()
    tgtgClient = initTgtgClientFromEnv()
    notifier = EmailNotifier([os.getenv("RECEIVER_EMAIL"), ])
    db = JsonDb(os.getenv("DB_BATH"))
    available_orders = tgtgClient.getAvailableToOrder()
    anyNew = addIfNotExists(available_orders, db)
    if anyNew:
        notifier.notify("Avaible order in your place.")
        logger.info("The notification send")
    else:
        logger.info("No new available order in your place.")


if __name__ == '__main__':
    run()
