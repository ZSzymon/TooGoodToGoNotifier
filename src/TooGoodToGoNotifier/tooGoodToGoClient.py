import json
import logging
import os

from dotenv import load_dotenv
from tgtg import TgtgClient, TgtgLoginError

from src.TooGoodToGoNotifier.exceptions import CredentialsFileNotExists
from src.TooGoodToGoNotifier.utils import saveToJson, print_list


def initTgtgClientFromEnv():
    load_dotenv()
    latitude = float(os.getenv("latitude".upper()))
    longitude = float(os.getenv("longitude".upper()))
    radius = int(os.getenv("radius".upper()))
    credentials_path = os.getenv("credentials_path".upper())
    tgtgClient = TooGoodToGoClient(latitude, longitude, radius, credentials_path)
    return tgtgClient


class TooGoodToGoClient:

    def __init__(self, latitude, longitude, radius, credentials_path):
        self.isLogged = False
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.credentials_path = credentials_path
        self.client = None
        self.logger = logging.getLogger(__name__)
        self.loginByTokens()

    def loginByEmail(self, email, verbose=False):
        client = TgtgClient(email=email)
        credentials = client.get_credentials()
        saveToJson(credentials, self.credentials_path)
        self.client = client
        self.isLogged = True

    def loginByTokens(self):
        credentials = self.readCredentials()
        accessToken = credentials['access_token']
        refresh_token = credentials['refresh_token']
        user_id = credentials['user_id']
        client = TgtgClient(access_token=accessToken, refresh_token=refresh_token, user_id=user_id)

        try:
            client.login()
            self.isLogged = True
            self.client = client
            self.logger.info("Logged to TGTG")
        except TgtgLoginError as e:
            self.logger.critical(e)

    def readCredentials(self):
        credentials_path = self.credentials_path
        if not os.path.isfile(credentials_path):
            raise CredentialsFileNotExists("Log in with email first.")

        with open(credentials_path, "r") as f:
            credentials = f.read()
            return json.loads(credentials)

    def getActive(self, verbose=True):
        ##Returns list of active (ordered, payed) orders.
        active = self.client.get_active()
        if verbose:
            print_list(active)
        return active

    def getInActive(self, verbose=True):
        # returns completed previous orders.
        inactive = self.client.get_inactive(0, 100)
        if verbose:
            print_list(inactive)

        return inactive

    def getAllInActive(self, verbose=True):
        page_size = 20
        orders = []
        current_page = 0
        while inactive := self.client.get_inactive(page=current_page, page_size=page_size):
            orders += inactive
            if not inactive["has_more"]:
                break
            current_page += 1

        return orders

    def getAllItems(self):
        page_size = 100
        items = []
        current_page = 1
        while items_chunk := self.client.get_items(page=current_page,
                                                   page_size=page_size,
                                                   latitude=self.latitude,
                                                   longitude=self.longitude,
                                                   favorites_only=False):
            items.extend(items_chunk)
            current_page += 1
        return items

    def getAvailableToOrder(self):
        a = [order for order in self.getAllItems() if order['items_available'] > 0]
        return a
