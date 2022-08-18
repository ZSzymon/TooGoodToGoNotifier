import os.path
import logging
from unittest import TestCase
from unittest.mock import Mock

from src.TooGoodToGoNotifier.tooGoodToGoClient import TooGoodToGoClient
from src.TooGoodToGoNotifier.utils import JsonDb, readToJson
from src.TooGoodToGoNotifier.main import initTgtgClientFromEnv, addIfNotExists


class TestDb(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = logging.getLogger(__name__)
        path = "test_db.json"
        if os.path.isfile(path):
            os.remove(path)

        cls.db = JsonDb(path)

    def setUpDb(self) -> JsonDb:
        path = "test_db.json"
        return JsonDb(path)

    def test_exist_success(self):
        id = 876543567854
        obj = " sdasd"
        isExist = self.db.exist(id)
        self.assertFalse(isExist)

    def test_exist_success2(self):
        id = 876543567854
        obj = " sdasd"
        self.db.addIfUnique(id, obj)
        isExist = self.db.exist(id)
        self.assertTrue(isExist)

    def test(self):
        db = self.setUpDb()
        tgtgClient = initTgtgClientFromEnv()
        tgtgClient.getAvailableToOrder = Mock()
        tgtgClient.getAvailableToOrder.return_value = readToJson("available.json")
        available_orders = tgtgClient.getAvailableToOrder()
        addIfNotExists(available_orders, db)

        anyNew = addIfNotExists(available_orders, db)
        if anyNew:
            self.logger.info("The notification send")
        else:
            self.logger.info("No available order in your place.")

        self.assertFalse(anyNew)