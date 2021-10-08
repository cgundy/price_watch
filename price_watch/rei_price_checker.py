import json
from typing import Dict, Generator, List, Optional, Union

from bs4 import BeautifulSoup
from pydantic import BaseModel
from price_watch.api_response import APIResponse
from price_watch.price_checker import PriceChecker


class ItemResponseREI(BaseModel):
    title: str
    sale: bool
    regularPrice: str
    salePrice: Optional[str]


class PriceCheckerREI(PriceChecker):
    def __init__(self):
        pass

    def _get_pricing_object(self, api_response_text: str) -> Union[str, bytes]:
        soup = BeautifulSoup(markup=api_response_text, features="html.parser")
        tag = soup.find(id="initial-props")
        if len(tag.contents) == 1:
            return tag.contents[0]
        else:
            raise ValueError

        # Todo: more specific errors for 0 or more than 1

    def _parse_prices(
        self, results: Union[str, bytes]
    ) -> Generator[ItemResponseREI, None, None]:
        items = json.loads(results)
        for item in items["ProductSearch"]["products"]["searchResults"]["results"]:
            title = item["title"]
            regularPrice = item["regularPrice"]
            salePrice = item["displayPrice"]["priceDisplay"]["salePrice"]

            yield ItemResponseREI(
                title=title,
                sale=salePrice is not None and regularPrice > salePrice,
                regularPrice=regularPrice,
                salePrice=salePrice,
            )

    def _check_sale(
        self, items: Generator[ItemResponseREI, None, None]
    ) -> List[ItemResponseREI]:
        return [item for item in items if item.sale]

    def get_sale_items(self, api_response_text: str) -> List[ItemResponseREI]:
        pricing_objects = self._get_pricing_object(api_response_text)
        items = self._parse_prices(pricing_objects)
        return self._check_sale(items)


def get_rei_response(
    pathname: str,
    query_params: Optional[Dict[str, str]] = None,
    protocol: str = "https",
    hostname: str = "www.rei.com",
) -> APIResponse:
    api_response = APIResponse(protocol, hostname)
    api_response.make_request(pathname, query_params)
    return api_response


# ProductSearch -> Products -> searchResults -> results -> displayPrice -> PriceDisplay -> SalePrice
