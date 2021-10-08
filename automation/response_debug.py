import json

from automation.rei_check_prices import item_2
from price_watch.rei_price_checker import (
    ItemResponseREI,
    PriceCheckerREI,
    get_rei_response,
)


api_response = get_rei_response(
    pathname=item_2.pathname, query_params=item_2.query_params
)
if not api_response.text:
    raise ValueError("No response text")

price_obj = PriceCheckerREI()._get_pricing_object(api_response.text)
items = json.loads(price_obj)["ProductSearch"]["products"]["searchResults"]["results"]
for item in items:
    print(
        ItemResponseREI(
            title=item["title"],
            sale=item["sale"],
            regularPrice=item["regularPrice"],
            salePrice=item["displayPrice"]["priceDisplay"]["salePrice"],
        )
    )
