from lxml import html
import requests


class BestBuyClient:

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

    def __init__(self):
        self.site = "https://www.bestbuy.com/"
        self.custom_header = self.HEADERS
        self.custom_header["Referer"] = self.site
        self.custom_header["Accept"] = "application/json"

    def check_availability(self, url) -> bool:
        if url is None:
            return False
        page = requests.get(url, headers=self.custom_header)
        doc = html.fromstring(page.content)
        raw_availability = doc.xpath('//*[contains(@class, "fulfillment-add-to-cart-button")]//text()')
        result = ''.join(raw_availability).strip() if raw_availability else None
        if result in 'Sold Out':
            return False
        if result in 'Add to cart':
            return True
        if result in 'Shop Open-Box':
            return False
        return False
