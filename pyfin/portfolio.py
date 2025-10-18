from __future__ import annotations
from typing import TYPE_CHECKING

import os

from astropy import units, time

from .sim import Simulation
from pyfin.etf.product import ETFProduct
from pyfin.etf.unit import ETFUnit
from pyfin import utils
if TYPE_CHECKING:
    from pyfin.container import Container

class Portfolio(Simulation):
    """The Portfolio actually contains only products, which themselves contain the units that make up a portfolio.
    """
    def __init__(self, path=None, **kwargs):
        super().__init__(path, **kwargs)
        self.product_directory = os.path.join(self.input_dir, "etf", "products")
        self.unit_directory = os.path.join(self.input_dir, "etf", "units")

        
    def load_etfs(self):
        for file in os.listdir(self.product_directory):
            path = os.path.join(self.product_directory, file)
            if os.path.isfile(path) and "template" not in file:
                self.message("Loading ETF Product from", path)
                etf_product = ETFProduct.from_file(path)
                self.add_item(etf_product)
        for product_name in os.listdir(self.unit_directory): # Directories containing unit files
            directory = os.path.join(self.unit_directory, product_name)
            self.message("Product units for", product_name, "from", directory)
            for file in os.listdir(directory): # Unit files
                path = os.path.join(directory, file)
                if os.path.isfile(path) and "template" not in file:
                    self.message("\tLoading ETF Unit from", path)
                    etf_product = self[product_name]
                    etf_unit = ETFUnit.from_file(path, container=etf_product)
                    etf_product.add_item(etf_unit)


    def write_etfs(self):
        for key, product in self._registry.items():
            for idn, unit in product._registry.items():
                unit.to_file()


    def add_etf_unit_ui(self):
        _, product = utils.select_option(
            message="Select a product:",
            options=self.list_items(),
        )
        product = self[product]
        purchased = utils.enter_time(
            message="Enter date purchased:"
        )
        price = utils.user_input(
            message="Enter price:",
            input_type=float
        )
        etf_unit = ETFUnit(
            container=product,
            purchased=purchased,
            price=price * utils.dollar
        )
        if isinstance(self.path, str):
            etf_unit.path = os.path.join(self.unit_directory, product.id, etf_unit.id + ".yaml")
            
        product.add_item(etf_unit)
        
                    
