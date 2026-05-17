from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from src.scraper import PriceScraper
from src.comparator import find_best_price


def create_driver():

    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    return driver


def main():

    product_keyword = input(
        "Enter product name: "
    )

    driver = create_driver()

    scraper = PriceScraper(driver)

    results = []

    try:

        results.append(
            scraper.search_amazon(product_keyword)
        )

        results.append(
            scraper.search_flipkart(product_keyword)
        )

        results.append(
            scraper.search_croma(product_keyword)
        )

    finally:
        driver.quit()

    print("\nPrice Comparison Results")
    print("-" * 40)

    for result in results:

        price = (
            result.get("price_text")
            or "Not found"
        )

        print(
            f"{result['website']}: {price}"
        )

    best_result = find_best_price(results)

    print("-" * 40)

    if best_result:

        print(
            f"Best option: "
            f"{best_result['website']} "
            f"at ₹{best_result['price']:,.0f}"
        )

    else:
        print("No valid price found")


if __name__ == "__main__":
    main()