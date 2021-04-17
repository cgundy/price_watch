from unittest import mock

import pytest

from price_watch.price_parser import PriceParserREI, ItemResponseREI


def test_get_pricing_object():
    soup = mock.Mock()
    soup.find().contents = []
    price_parser = PriceParserREI(soup)

    with pytest.raises(ValueError) as e:
        price_parser.get_pricing_object()
    soup.find.assert_called_with(id="initial-props")


@mock.patch("price_watch.price_parser.json.loads")
def test_parse_prices(json_loader):
    soup = mock.Mock()
    results = mock.Mock()
    json_loader["ProductSearch"]["products"]["searchResults"][
        "results"
    ].return_value = [
        {
            "title": "Some cool backpack",
            "sale": False,
            "regularPrice": "$29",
            "salePrice": None,
        }
    ]
    price_parser = PriceParserREI(soup)
    items = price_parser.parse_prices(results)
    for item in items:
        assert item == [
            ItemResponseREI(
                title="Some cool backpack",
                sale=False,
                regularPrice="$29",
                salePrice=None,
            )
        ]


@mock.patch("price_watch.price_parser.ItemResponseREI")
def test_check_sale(item_response):
    soup = mock.Mock()
    item_response.sale = False
    price_parser = PriceParserREI(soup)
    assert price_parser.check_sale([item_response]) == []
    item_response.sale = True
    assert len(price_parser.check_sale([item_response])) > 0