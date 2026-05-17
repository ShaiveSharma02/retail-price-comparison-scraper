import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.scraper import PriceScraper
from src.comparator import find_best_price


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver


st.set_page_config(
    page_title="Retail Price Comparison Tool",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Retail Price Comparison Tool")

st.write(
    "Compare product prices across Amazon, Flipkart, and Croma using Python web scraping."
)

product_keyword = st.text_input(
    "Enter product name",
    placeholder="Example: iPhone 16 128 GB"
)

if st.button("Compare Prices"):

    if not product_keyword:
        st.warning("Please enter a product name.")
    else:
        with st.spinner("Searching prices across websites..."):
            driver = create_driver()
            scraper = PriceScraper(driver)

            results = []

            try:
                results.append(scraper.search_amazon(product_keyword))
                results.append(scraper.search_flipkart(product_keyword))
                results.append(scraper.search_croma(product_keyword))
            finally:
                driver.quit()

        st.subheader("Price Comparison Results")

        col1, col2, col3 = st.columns(3)

        websites = ["Amazon", "Flipkart", "Croma"]
        columns = [col1, col2, col3]

        for website, col in zip(websites, columns):
            result = next(
                item for item in results
                if item["website"] == website
            )

            price_text = result.get("price_text") or "Not found"

            col.metric(
                label=website,
                value=price_text
            )

        best_result = find_best_price(results)

        if best_result:
            st.success(
                f"Best price found on {best_result['website']} "
                f"at ₹{best_result['price']:,.0f}"
            )
        else:
            st.error("No valid price found.")