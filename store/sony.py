import time

from lxml import html
import requests


class Sony:

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

    def __init__(self):
        self.site = "https://direct.playstation.com/en-us/"
        self.custom_header = self.HEADERS
        self.custom_header["Referer"] = self.site
        self.custom_header["Accept"] = "application/json"

    def check_availability(self) -> bool:
        page = requests.get("https://direct.playstation.com/en-us/consoles/console/playstation5-digital-edition-console.3005817", headers=self.custom_header)
        doc = html.fromstring(page.content)
        raw_availability = doc.xpath('//div[@id ="lbHeaderH2"]//text()')
        result = ''.join(raw_availability).strip() if raw_availability else None
        if str(result) in str('We’re trying to get you in'):
            return True
        return False
