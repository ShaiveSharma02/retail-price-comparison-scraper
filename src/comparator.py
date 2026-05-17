def find_best_price(price_results):

    valid_results = [
        result for result in price_results
        if result.get("price") is not None
    ]

    if not valid_results:
        return None

    return min(valid_results, key=lambda x: x["price"])