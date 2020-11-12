from bestbuy import BestBuyAPI
from bs4 import BeautifulSoup


class BestBuyClient:

    def __init__(self):
        self.bb = BestBuyAPI("apiToken")

    def search_products_by_sku(self, sku: str = None):
        return self.bb.products.search(query=f"sku={sku}", format="json")

    def search_products_by_category(self, category_id: str = None):
        return self.bb.category.search_by_id(category_id=f"{category_id}", format="json")

    def get_all_categories(self):
        return self.bb.bulk.archive("categories", "json")

    @staticmethod
    def check_availability(product_info, webdriver) -> bool:
        try:
            # Get the contents of the URL
            webdriver.get(product_info["bestbuy_link"])

            # returns the inner HTML as a string
            inner_html = webdriver.page_source

            # turns the html into an object to use with BeautifulSoup library
            soup = BeautifulSoup(inner_html, "html.parser")
            tag = soup.find('button', "add-to-cart-button")
            if tag.text == "Coming Soon":
                return False
            if tag.text == "Add to cart":
                return True
        except:
            print("Nothing worked")

        return False
