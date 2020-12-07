# Python script for Amazon product availability checker
# importing libraries
from lxml import html
import requests


class Amazon:

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }

    def __init__(self):
        self.site = "http://www.amazon.com/dp/"
        self.custom_header = self.HEADERS
        self.custom_header["Referer"] = self.site
        self.custom_header["Accept"] = "application/json"

    def check_availability(self, url) -> bool:
        if url is None:
            return False
        page = requests.get(url, headers=self.custom_header)
        doc = html.fromstring(page.content)

        # checking availability
        xpath_availability = '//div[@id ="availability"]//text()'
        raw_availability = doc.xpath(xpath_availability)
        ans = ''.join(raw_availability).strip().rstrip() if raw_availability else None
        if str(ans).lower() in "In Stock.".lower():
            return True
        if str(ans).lower() in "Only 2 left in stock.".lower():
            return True
        if str(ans).lower() in "Only 1 left in stock.".lower():
            return True
        return False
