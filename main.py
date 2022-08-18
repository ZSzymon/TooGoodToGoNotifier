# Press the green button in the gutter to run the script.
from src.TooGoodToGoNotifier.tooGoodToGoClient import TooGoodToGoClient
import logging
if __name__ == '__main__':
    # # 21.0183676,
    # # "latitude": 52.2168242
    # lublin_latitude = 51.249311
    # lublin_longitude = 22.530318
    # warsaw_latitude = 52.21554
    # warsaw_longitude = 21.01907
    # radious = 10
    # tgtgClient = TooGoodToGoClient(warsaw_latitude, warsaw_longitude, radious)
    # # tgtgClient = TooGoodToGoClient(lublin_latitude, lublin_longitude, 15)
    # # tgtgClient.loginByEmail('szymonzywko@gmail.com')
    # tgtgClient.loginByTokens()
    # # myActive = tgtgClient.getActive(True)
    # items = tgtgClient.getItems(True)
    # # itemsInActive = tgtgClient.getInActive(True)
    # # saveToJson(itemsInActive, "history.json")
    #
    # # saveToJson(items, "itemsAvaible15kmWarsaw.json")
    # saveToJson(items, f"allItemsWarsaw{radious}km.json")

    path = "D:\\Szymon\\programming\\python\\TooGoodToGoNotifier\\example.log"
    logging.basicConfig(filename=path, encoding='utf-8', level=logging.DEBUG)
    logging.debug("Debug logging test...")
    logger = logging.getLogger("TestLogger")
    logger.critical("Dupa")

    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
