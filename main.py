#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import logging.config

from messenger.groupme import GroupMe
from store.amazon import Amazon
from store.bestbuy import BestBuyClient
from store.newegg import NewEgg
from store.sony import Sony
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
        "amazon_ID": "B08FC6MR62",
        "amazon_link": "https://www.amazon.com/dp/B08FC6MR62/",
    },
    {
        "name": "PS5 full",
        "target_ID": "81114595",
        "target_link": "https://www.target.com/p/playstation-5-console/-/A-81114595",
        "walmart_ID": "363472942",
        "walmart_link": "https://www.walmart.com/ip/PlayStation-5-Console/363472942",
        "bestbuy_ID": "6426149",
        "bestbuy_link": "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149",
        "amazon_ID": "B08FC5L3RG",
        "amazon_link": "https://www.amazon.com/dp/B08FC5L3RG/",
        "newegg_ID": "N82E16868110292",
        "newegg_link": "https://www.newegg.com/p/N82E16868110292",
    },
    {
        "name": "Xbox Series X",
        "target_ID": "80790841",
        "target_link": "https://www.target.com/p/xbox-series-x-console/-/A-80790841#lnk=sametab",
        "walmart_ID": "443574645",
        "walmart_link": "https://www.walmart.com/ip/XB1-Xbox-Series-X/443574645",
        "bestbuy_ID": "6428324",
        "bestbuy_link": "https://www.bestbuy.com/site/microsoft-xbox-series-x-1tb-console-black/6428324.p?skuId=6428324",
        "amazon_ID": "B08H75RTZ8",
        "amazon_link": "https://www.amazon.com/dp/B08H75RTZ8",
        "newegg_ID": "N82E16868105273",
        "newegg_link": "https://www.newegg.com/p/N82E16868105273",
    },
]


def check_store(logger, client, store_name, store_link, product_name, group_me):
    store = store_name
    logger.info(f"Checking {store}")
    result = client.check_availability(store_link)
    if result:
        group_me.send_message(f"{product_name} is available at {store}!!!")
        link = store_link
        group_me.send_message(link)
    else:
        logger.info("Not available")


def main():
    logging.config.fileConfig('/Users/plosco/code/python/operationPS5/logging.conf')
    logger = logging.getLogger(__name__)
    group_me = GroupMe()
    target = TargetClient()
    amazon = Amazon()
    bestbuy = BestBuyClient()
    walmart = Walmart()
    newegg = NewEgg()

    # if Sony().check_availability():
    #     logger.info("there is a queue")
    #     group_me.send_message(f"get in line")
    #     group_me.send_message("https://direct.playstation.com/en-us/consoles/console/playstation5-digital-edition-console.3005817")
    # else:
    #     logger.info("Not available directly")

    for product_info in PRODUCT_INFOS:
        product_name = product_info["name"]
        logger.info("Checking: " + product_name)

        try:
            logger.info("Checking Target")
            amount = target.check_availability(product_info)
            if amount > 0:
                logger.info(f"{amount} units found")
                group_me.send_message(f"{product_name} is available at target!!! {amount} units left in stock")
                link = product_info["target_link"]
                group_me.send_message(link)
            else:
                logger.info("Not available")

            store = "Amazon"
            store_link = "amazon_link"
            check_store(logger, amazon, store, product_info[store_link], product_name, group_me)

            store = "BesBuy"
            store_link = "bestbuy_link"
            check_store(logger, bestbuy, store, product_info[store_link], product_name, group_me)

            store = "Walmart"
            store_link = "walmart_link"
            check_store(logger, walmart, store, product_info[store_link], product_name, group_me)

            store = "NewEgg"
            store_link = "newegg_link"
            check_store(logger, newegg, store, product_info[store_link], product_name, group_me)
        except KeyError:
            logger.error("could not find something in the list")


if __name__ == '__main__':
    main()
