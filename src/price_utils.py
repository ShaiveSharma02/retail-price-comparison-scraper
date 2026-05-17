import re


def extract_numeric_price(price_text):

    if not price_text:
        return None

    cleaned_price = re.sub(r"[^\d]", "", price_text)

    if not cleaned_price:
        return None

    return float(cleaned_price)