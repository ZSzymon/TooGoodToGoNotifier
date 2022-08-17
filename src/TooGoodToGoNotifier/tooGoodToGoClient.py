import json
import os

from tgtg import TgtgClient

from src.TooGoodToGoNotifier.exceptions import CredentialsFileNotExists
from src.TooGoodToGoNotifier.utils import saveToJson, print_list


class TooGoodToGoClient:

    def __init__(self, latitude, longitude, radius, credentials_path):
        self.isLogged = False
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.credentials_path = credentials_path
        self.client = None

    def loginByEmail(self, email, verbose=False):
        client = TgtgClient(email=email)
        credentials = client.get_credentials()
        saveToJson(credentials, self.credentials_path)

        if verbose:
            print(credentials)

        self.client = client
        self.isLogged = True

    def loginByTokens(self):
        credentials = self.readCredentials()
        accessToken = credentials['access_token']
        refresh_token = credentials['refresh_token']
        user_id = credentials['user_id']

        client = TgtgClient(access_token=accessToken, refresh_token=refresh_token, user_id=user_id)
        self.client = client
        self.isLogged = True

    def readCredentials(self):
        credentails_file_path = self.credentials_path
        if not os.path.isfile(credentails_file_path):
            raise CredentialsFileNotExists("Log in with email first.")

        with open(credentails_file_path, "r") as f:
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
        page_size = 350
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

    def my_history_example(self):
        orders = self.getAllInActive()

        redeemed_orders = [x for x in orders if x["state"] == "REDEEMED"]
        redeemed_items = sum([x["quantity"] for x in redeemed_orders])

        # if you bought in multiple currencies this will need improvements
        money_spend = sum(
            [
                x["price_including_taxes"]["minor_units"]
                / (10 ** x["price_including_taxes"]["decimals"])
                for x in redeemed_orders
            ]
        )

        print(f"Total numbers of orders: {len(orders)}")
        print(f"Total numbers of picked up orders: {len(redeemed_orders)}")
        print(f"Total numbers of items picked up: {redeemed_items}")
        print(
            f"Total money spend: ~{money_spend:.2f}{redeemed_orders[0]['price_including_taxes']['code']}"
        )

    def getAvailableToOrder(self):
        a = [order for order in self.getAllItems() if order['items_available'] > 0]

        return a
