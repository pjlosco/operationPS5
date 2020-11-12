import requests
import urllib.request
import urllib.parse
import json


class TargetClient:


    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
    }

    def __init__(self):
        s = requests.session()
        s.get('https://www.target.com')

        key = s.cookies['visitorId']
        location = s.cookies['GuestLocation'].split('|')[0]

        store_id = requests.get(
            'https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile' % (
                location, key)).json()
        self.store_id = store_id[0]['locations'][0]['location_id']
        self.custom_header = self.HEADERS
        self.custom_header["Referer"] = "https://target.com/"
        self.custom_header["Accept"] = "application/json"

    def check_availability(self, product_info) -> int:
        product_id = product_info["target_ID"]
        url = f"https://redsky.target.com/v1/location_details/{product_id}?zip=92694&state=CA&storeId={self.store_id}"
        req = urllib.request.Request(url, headers=self.custom_header)
        response = urllib.request.urlopen(req).read().decode()
        data = json.loads(response)
        status = data["product"]["available_to_promise_store"]["products"][0]["availability_status"]
        if status == "OUT_OF_STOCK":
            status = data["product"]["available_to_promise_network"]["availability_status"]
            if status == "OUT_OF_STOCK":
                return 0
            elif status == "IN_STOCK":
                return int(data["product"]["available_to_promise_network"]["available_to_promise_quantity"])
            elif status == "PRE_ORDER_SELLABLE":
                return int(data["product"]["available_to_promise_network"]["available_to_promise_quantity"])
        elif status == "IN_STOCK":
            return int(data["product"]["available_to_promise_store"]["products"][0]["available_to_promise_quantity"])
        elif status == "PRE_ORDER_SELLABLE":
            return int(data["product"]["available_to_promise_store"]["products"][0]["available_to_promise_quantity"])

        print("Unknown status.")
        return False



