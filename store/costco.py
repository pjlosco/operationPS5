import urllib.request
import urllib.parse
import json


class CostcoClient:
    PRODUCT_INFOS = [
        {
            "name": "PS5 Digital",
            "url": "https://www.costco.com/AjaxGetContractPrice?itemId=507802&catalogId=10701&productId=507801&WH=XXXXXX",
        },

    ]

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
    }

    def __init__(self):
        print("Costco")
        self.custom_header = self.HEADERS
        self.custom_header["Referer"] = "https://costco.com/"
        self.custom_header["Accept"] = "application/json"

    def is_available(self) -> bool:
        print("Costco")
        for product_info in self.PRODUCT_INFOS:
            print("Check: " + product_info["name"])
            is_available = self.__check_availability(product_info)
            if is_available:
                return True
            else:
                print("Not available.")

        return False

    def __check_availability(self, product_info):
        # This seems to work only with 2-day-shipping products.
        # A product's page loads with initial inventory availability info set,
        # but the 2-day-shipping products override this info with a subsequent xhr.
        # Need to look into this a little more when I have time.
        # This currently works for Kirkland TP, though, so good enough for now.

        # Assemble and submit the request.
        req = urllib.request.Request(product_info["url"], headers=self.custom_header)
        response = urllib.request.urlopen(req).read().decode()

        # Parse the json response into usable data.
        data = json.loads(response)

        if "invAvailable" in data:
            status = data["invAvailable"]  # boolean
            return status

        print("Unknown status.")
        return False

