from lxml import html
import requests


class Gamestop:

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

    def __init__(self):
        self.site = "https://www.gamestop.com/"
        self.custom_header = self.HEADERS
        self.custom_header["Referer"] = self.site
        self.custom_header["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        self.custom_header["authority"] = "9300303.fls.doubleclick.net"
        self.custom_header["scheme"] = "https"
        self.custom_header["sec-fetch-dest"] = "iframe"
        self.custom_header["sec-fetch-mode"] = "navigate"
        self.custom_header["sec-fetch-site"] = "cross-site"

    def check_availability(self, url) -> bool:
        if url is None:
            return False
        page = requests.get(url, headers=self.custom_header)
        if page.status_code > 300:
            return False
        doc = html.fromstring(page.content)
        raw_availability = doc.xpath('//div[contains(@class, "primary-details-row")]//button[contains(@class, "add-to-cart")]//text()')

        result = ''.join(raw_availability).strip() if raw_availability else None
        if str(result).lower() in str("Not Available").lower():
            return False
        if str(result).lower() in str("Add to cart").lower():
            return True
        return False
