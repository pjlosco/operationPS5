from bs4 import BeautifulSoup, NavigableString


class Walmart:

    @staticmethod
    def check_availability(product_info, webdriver) -> bool:
        # Get the contents of the URL
        webdriver.get(product_info["walmart_link"])

        # returns the inner HTML as a string
        inner_HTML = webdriver.page_source

        # turns the html into an object to use with BeautifulSoup library
        soup = BeautifulSoup(inner_HTML, "html.parser")
        tag = soup.find('span', "spin-button-children")
        if tag == None:
            return False
        if tag.text == "Add to cart":
            return True
        return False

