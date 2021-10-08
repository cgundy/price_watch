from typing import Dict, Generator, List, Union


class PriceChecker:
    def _get_pricing_object(self, api_response_text: str) -> Union[str, bytes]:
        raise NotImplementedError

    def _parse_prices(self, results: Union[str, bytes]) -> Generator:
        raise NotImplementedError

    def _check_sale(self, items: Generator) -> List:
        raise NotImplementedError

    def get_sale_items(self, api_response_text: str) -> List:
        raise NotImplementedError
