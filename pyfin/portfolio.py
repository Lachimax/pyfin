from __future__ import annotations
from typing import TYPE_CHECKING

import os

from astropy import units, time

from .sim import Simulation
from pyfin.etf.product import ETFProduct
from pyfin.etf.unit import ETFUnit
if TYPE_CHECKING:
    from pyfin.container import Container

class Portfolio(Simulation):
    """The Portfolio actually contains only products, which themselves contain the units that make up a portfolio.
    """
    def __init__(self, path=None, **kwargs):
        super().__init__(path, **kwargs)
        
    def load_etfs(self):
        product_directory = os.path.join(self.input_dir, "etf", "products")
        for file in os.listdir(product_directory):
            path = os.path.join(product_directory, file)
            if os.path.isfile(path):
                etf_product = ETFProduct.from_file(path)
                self.add_item(etf_product)
        unit_directory = os.path.join(self.input_dir, "etf", "units")
        for product_name in os.listdir(unit_directory): # Directories containing unit files
            directory = os.path.join(unit_directory, product_name)
            for file in os.listdir(directory): # Unit files
                path = os.path.join(unit_directory, file)
                if os.path.isfile(path):
                    etf_product = self[product_name]
                    etf_unit = ETFUnit.from_file(path)
                    etf_product.add_item(etf_unit)
                    
