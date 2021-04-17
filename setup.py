from setuptools import setup, find_packages

setup(
    name="price_watch",
    packages=find_packages(),
    version="0.0.1",
    entry_points={
        "console_scripts": ["rei_check = automation.rei_price_check:get_REI_sale_items"]
    },
)