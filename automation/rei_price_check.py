from typing import Dict, List, Optional

from price_watch.api_call import url_constructor, APIResponse
from price_watch.price_parser import get_REI_sales, ItemResponseREI

# url = "https://www.rei.com/c/climbing-ropes?ir=category%3Aclimbing-ropes"
# url = "https://www.rei.com/c/hiking-backpacks?ir=category%3Ahiking-backpacks&r=c%3Bgender%3AWomen%27s%3Bgear-capacity-l%3A21+to+35"

protocol = "https"
hostname = "www.rei.com"

rei_item_checks = [
    {
        "name": "hiking_backpacks",
        "pathname": "c/hiking-backpacks",
        "query_parameters": {
            "ir": "category:hiking-backpacks",
            "r": "c;gender:Women's;gear-capacity-l:21 to 35",
        },
    },
    {
        "name": "climbing_ropes",
        "pathname": "c/climbing-ropes",
        "query_parameters": None,
    },
]


def get_REI_sale_items(
    item_checks: List[Dict] = rei_item_checks,
) -> List[Optional[ItemResponseREI]]:
    sale_items = []
    for item_check in item_checks:
        rei_response = APIResponse(
            url_constructor(protocol, hostname, item_check["pathname"]),
            item_check["query_parameters"],
        )
        text = rei_response.get_text()
        url = rei_response.get_url()
        print(url)
        sale_items.append(get_REI_sales(text))
    return sale_items