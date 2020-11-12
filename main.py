from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import logging
import logging.config

from messenger.groupme import GroupMe
from store.bestbuy import BestBuyClient
from store.target import TargetClient
from store.walmart import Walmart

PRODUCT_INFOS = [
    {
        "name": "PS5 Digital",
        "target_ID": "81114596",
        "target_link": "https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596",
        "walmart_ID": "493824815",
        "walmart_link": "https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815",
        "bestbuy_ID": "6430161",
        "bestbuy_link": "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161",
    },
    {
        "name": "PS5 full",
        "target_ID": "81114595",
        "target_link": "https://www.target.com/p/playstation-5-console/-/A-81114595",
        "walmart_ID": "363472942",
        "walmart_link": "https://www.walmart.com/ip/PlayStation-5-Console/363472942",
        "bestbuy_ID": "6426149",
        "bestbuy_link": "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149",
    },
]


def selenium_driver_setup():
    print("Setting up login via selenium")
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    # options.add_argument('--incognito')
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def main():
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)
    group_me = GroupMe()
    target = TargetClient()
    # driver = selenium_driver_setup()

    while True:
        for product_info in PRODUCT_INFOS:
            name = product_info["name"]
            logger.info("Checking: " + name)

            logger.info("Checking Target")
            amount = target.check_availability(product_info)
            if amount > 0:
                logger.info(f"{amount} units found")
                group_me.send_message(f"{name} is available at target!!! {amount} units left in stock")
                link = product_info["target_link"]
                group_me.send_message(link)
                return
            else:
                logger.info("Not available")
            
            # logger.info("Checking Walmart")
            # in_stock = Walmart().check_availability(product_info, driver)
            # if in_stock:
            #     group_me.send_message(f"{name} is available at Walmart!!!")
            #     link = product_info["walmart_link"]
            #     group_me.send_message(link)
            # else:
            #     logger.info("Not available")

            # logger.info("Checking BestBuy")
            # in_stock = BestBuyClient().check_availability(product_info, driver)
            # if in_stock:
            #     group_me.send_message(f"{name} is available at BestBuy!!!")
            #     link = product_info["bestbuy_link"]
            #     group_me.send_message(link)
            # else:
            #     logger.info("Not available")

        logger.info("Waiting a minute to check again")
        time.sleep(500)


if __name__ == '__main__':
    main()
