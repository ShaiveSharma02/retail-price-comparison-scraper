from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.price_utils import extract_numeric_price


class PriceScraper:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def search_amazon(self, keyword):

        try:
            self.driver.get("https://www.amazon.in")

            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.ID, "twotabsearchtextbox")
                )
            )

            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)

            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span.a-price-whole")
                )
            )

            soup = BeautifulSoup(
                self.driver.page_source,
                "html.parser"
            )

            price_element = soup.select_one(
                "span.a-price-whole"
            )

            price_text = (
                price_element.get_text(strip=True)
                if price_element else None
            )

            return {
                "website": "Amazon",
                "price_text": price_text,
                "price": extract_numeric_price(price_text)
            }

        except Exception as error:

            return {
                "website": "Amazon",
                "price_text": None,
                "price": None,
                "error": str(error)
            }

    def search_flipkart(self, keyword):

        try:
            self.driver.get("https://www.flipkart.com")

            # Close login popup if it appears
            try:
                close_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//span[text()='✕']")
                    )
                )
                close_button.click()
            except Exception:
                pass

            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.NAME, "q")
                )
            )

            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div[class*='Nx9bqj'], div._30jeq3, div._1_WHN1"
                    )
                )
            )

            soup = BeautifulSoup(
                self.driver.page_source,
                "html.parser"
            )

            price_selectors = [
                "div.Nx9bqj.CxhGGd",
                "div.Nx9bqj",
                "div._30jeq3",
                "div._1_WHN1",
                "div[class*='Nx9bqj']"
            ]

            price_element = None

            for selector in price_selectors:
                price_element = soup.select_one(selector)

                if price_element:
                    break

            price_text = (
                price_element.get_text(strip=True)
                if price_element else None
            )

            return {
                "website": "Flipkart",
                "price_text": price_text,
                "price": extract_numeric_price(price_text)
            }

        except Exception as error:

            return {
                "website": "Flipkart",
                "price_text": None,
                "price": None,
                "error": str(error)
            }

    def search_croma(self, keyword):

        try:
            self.driver.get("https://www.croma.com")

            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.ID, "searchV2")
                )
            )

            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)

            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span.amount")
                )
            )

            soup = BeautifulSoup(
                self.driver.page_source,
                "html.parser"
            )

            price_element = soup.select_one(
                "span.amount"
            )

            price_text = (
                price_element.get_text(strip=True)
                if price_element else None
            )

            return {
                "website": "Croma",
                "price_text": price_text,
                "price": extract_numeric_price(price_text)
            }

        except Exception as error:

            return {
                "website": "Croma",
                "price_text": None,
                "price": None,
                "error": str(error)
            }