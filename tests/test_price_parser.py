from unittest import mock

import pytest

from price_watch.rei_price_checker import PriceCheckerREI, ItemResponseREI


@mock.patch("price_watch.rei_price_checker.BeautifulSoup")
def test_get_pricing_object_raises_error(soup):
    soup().find().contents = []
    price_parser = PriceCheckerREI()

    with pytest.raises(ValueError) as e:
        price_parser._get_pricing_object(mock.Mock())


@mock.patch("price_watch.rei_price_checker.BeautifulSoup")
def test_get_pricing_object_called_with(soup):
    soup().find().contents = ["some content"]
    price_parser = PriceCheckerREI()

    price_parser._get_pricing_object(mock.Mock())

    soup().find.assert_called_with(id="initial-props")


@mock.patch("price_watch.rei_price_checker.json.loads")
def test_parse_prices(json_loader: mock.Mock):
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
    price_parser = PriceCheckerREI()

    items = price_parser._parse_prices(results)

    for item in items:
        assert item == [
            ItemResponseREI(
                title="Some cool backpack",
                sale=False,
                regularPrice="$29",
                salePrice=None,
            )
        ]


def test_check_sale():
    item_response = ItemResponseREI(
        title="some title", sale=False, regularPrice=100, salePrice=None
    )
    price_parser = PriceCheckerREI()
    assert price_parser._check_sale([item_response]) == []

    item_response.sale = True
    item_response.salePrice = 80
    assert len(price_parser._check_sale([item_response])) > 0
