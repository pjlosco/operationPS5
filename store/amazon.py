# Python script for Amazon product availability checker
# importing libraries
from lxml import html
import requests


class Amazon:

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

    def __init__(self):
        self.site = "http://www.amazon.in/dp/"
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
        ans = ''.join(raw_availability).strip() if raw_availability else None
        arr = [
            'Only 1 left in stock.',
            'Only 2 left in stock.',
            'In stock.']
        if ans in arr:
            return True
        return False
