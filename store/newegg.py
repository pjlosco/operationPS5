import time

from lxml import html
import requests


class NewEgg:

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

    def __init__(self):
        self.site = "https://www.newegg.com/"
        self.custom_header = self.HEADERS
        self.custom_header["Referer"] = self.site
        self.custom_header["Accept"] = "application/json"

    def check_availability(self, url) -> bool:
        if url is None:
            return False
        page = requests.get(url, headers=self.custom_header)
        doc = html.fromstring(page.content)
        try:
            raw_availability = doc.xpath('//div[@id ="ProductBuy"]//span[contains(@class, "btn-message")]//text()')
            result = ''.join(raw_availability).strip() if raw_availability else None
            if str(result) in str("Sold Out"):
                return False
            raw_availability = doc.xpath('//div[contains(@class, "flags-body")]//text()')
            result = ''.join(raw_availability).strip() if raw_availability else None
            if str(result) in str("CURRENTLY SOLD OUT"):
                return False
        except:
            time.sleep(1)

        raw_availability = doc.xpath('//div[@id ="ProductBuy"]//button[contains(@class, "btn-primary")]//text()')
        result = ''.join(raw_availability).strip() if raw_availability else None
        if str(result) in str("Add to cart"):
            return True
        return False
