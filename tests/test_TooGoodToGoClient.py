import enum
from enum import Enum
from unittest import TestCase
from src.tooGoodToGoNotifier.tooGoodToGoClient import TooGoodToGoClient


class CITY(Enum):
    LUBLIN = enum.auto()
    WARSAW = enum.auto()


class TestTGTG(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cityOptions = {CITY.LUBLIN: self.getLublinClient,
                            CITY.WARSAW: self.getWarsawClient}


    def getLublinClient(self):
        credentials_path = "../credentails.json"
        lublin_latitude = 51.249311
        lublin_longitude = 22.530318
        warsaw_latitude = 52.21554
        warsaw_longitude = 21.01907
        radius = 1
        tgtgClient = TooGoodToGoClient(lublin_latitude, lublin_longitude, radius, credentials_path)

        return tgtgClient

    def getWarsawClient(self):
        credentials_path = "../credentails.json"
        warsaw_latitude = 52.21554
        warsaw_longitude = 21.01907
        radius = 5
        tgtgClient = TooGoodToGoClient(warsaw_latitude, warsaw_longitude, radius, credentials_path)

        return tgtgClient

    def getLoggedClient(self, city=CITY.LUBLIN):
        properClient = self.cityOptions[city]
        tgtgClient = properClient()
        tgtgClient.loginByTokens()
        return tgtgClient

    def test_login(self):
        self.assertIsNotNone(self.getLoggedClient())

    def test_getAllItems(self):
        client: TooGoodToGoClient = self.getLoggedClient()
        items = client.getAllItems()
        self.assertIsNotNone(items)

    def test_getAllInactiveOrders(self):
        client: TooGoodToGoClient = self.getLoggedClient()
        in_active = client.getAllInActive()

    def test_getItemsWithAvailableItems(self):
        client: TooGoodToGoClient = self.getLoggedClient(CITY.WARSAW)
        available = client.getAvailableToOrder()





