from collections import namedtuple
from typing import Dict, List

from requests.models import HTTPError


from price_watch.rei_price_checker import PriceCheckerREI, get_rei_response


REI_items = namedtuple("REI_items", "name pathname query_params")
item_1 = REI_items(
    "hiking_backpacks",
    "c/hiking-backpacks",
    {
        "ir": "category:hiking-backpacks",
        "r": "c;gender:Women's;gear-capacity-l:21 to 35",
    },
)
item_2 = REI_items("climbing_ropes", "c/climbing-ropes", None)


def get_REI_sale_items(items: List[REI_items]) -> Dict:
    all_sale_items: Dict = {}
    for item in items:
        api_response = get_rei_response(
            pathname=item.pathname, query_params=item.query_params
        )
        if api_response.status_code != 200:
            raise HTTPError(
                f"{api_response.status_code} {api_response.reason} for {api_response.url}"
            )
        if not api_response.text:
            raise ValueError("No response text")

        sale_items = PriceCheckerREI().get_sale_items(api_response.text)
        all_sale_items[item.name] = {}
        all_sale_items[item.name]["url"] = api_response.url
        all_sale_items[item.name]["sale_items"] = sale_items
    return all_sale_items


print(get_REI_sale_items([item_1, item_2]))
