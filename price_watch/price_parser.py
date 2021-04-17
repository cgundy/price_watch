import json
from typing import Any, Dict, Generator, List, Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel


class ItemResponseREI(BaseModel):
    title: str
    sale: bool
    regularPrice: str
    salePrice: Optional[str]


class PriceParser:
    def get_pricing_object(self) -> Dict:
        raise NotImplementedError

    def parse_prices(self, results: Dict) -> Generator:
        raise NotImplementedError


class PriceParserREI(PriceParser):
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def get_pricing_object(self) -> Dict:
        tag = self.soup.find(id="initial-props")
        if len(tag.contents) == 1:
            return tag.contents[0]
        else:
            raise ValueError

        # Todo: more specific errors for 0 or more than 1

    def parse_prices(self, results: Any) -> Generator[ItemResponseREI, None, None]:
        items = json.loads(results)
        for item in items["ProductSearch"]["products"]["searchResults"]["results"]:

            yield ItemResponseREI(
                title=item["title"],
                sale=item["sale"],
                regularPrice=item["regularPrice"],
                salePrice=item["displayPrice"]["priceDisplay"]["salePrice"],
            )

    def check_sale(
        self, items: Generator[ItemResponseREI, None, None]
    ) -> List[Optional[ItemResponseREI]]:
        return [item for item in items if item.sale]


def get_REI_sales(text_file: str) -> List[Optional[ItemResponseREI]]:
    response_parser = PriceParserREI(
        BeautifulSoup(markup=open(text_file), features="html.parser")
    )
    pricing_object = response_parser.get_pricing_object()
    return response_parser.check_sale(response_parser.parse_prices(pricing_object))


# ProductSearch -> Products -> searchResults -> results -> displayPrice -> PriceDisplay -> SalePrice
