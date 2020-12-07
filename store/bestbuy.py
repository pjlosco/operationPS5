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
        raw_availability = doc.xpath('//div[contains(@class, "fulfillment-add-to-cart-button")]//button[contains(@class, "add-to-cart-button")]//text()')
        result = ''.join(raw_availability).strip() if raw_availability else None
        if str(result).lower() in str("Sold Out").lower():
            return False
        if str(result).lower() in str("Add to cart").lower():
            return True
        if str(result).lower() in str("Shop Open-Box").lower():
            return False
        return False
