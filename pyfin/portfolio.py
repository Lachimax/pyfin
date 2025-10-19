from __future__ import annotations
from typing import TYPE_CHECKING

import os

from astropy import units, time
from astropy.table import QTable

from .sim import Simulation
from pyfin.etf.product import ETFProduct
from pyfin.etf.unit import ETFUnit
from pyfin import utils
from astropy.table import vstack
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

        print()


    def write_etfs(self):
        for key, product in self._registry.items():
            for idn, unit in product._registry.items():
                unit.to_file()


    def add_etf_units_ui(self):
        purchased = utils.enter_time(
            message="Enter date of transaction:"
        )
        added = []
        cont = True
        while cont:
            _, product_name = utils.select_option(
                message="Select a product:",
                options=self.list_items(),
            )
            product = self[product_name]
            price = utils.user_input(
                message=f"Enter unit price of {product_name}:",
                input_type=float
            )
            n = utils.user_input(
                message=f"How many {product_name} units were purchased in this transaction?",
                input_type=int
            )
            i = 0
            while i < n:
                etf_unit = ETFUnit(
                    container=product,
                    purchased=purchased,
                    price=price * utils.dollar
                )
                i += 1
                product.add_item(etf_unit)
                added.append(product_name)
            added.sort()
            for p in added:
                print(p)
            # for key, product in self._registry.items():
            #     for item in product._registry:
            #         print(item)
            cont = utils.select_yn("Were other products purchased in this transaction?")

    def collect_dicts(self):
        dicts = []
        for name, product in self._registry.items():
            dicts += product.collect_dicts()
        return dicts

    def tabulate(self):
        all_table = QTable(self.collect_dicts())
        if isinstance(self.input_dir, str):
            all_table.write(os.path.join(self.input_dir, f"{self.name}.ecsv"))
            all_table.write(os.path.join(self.input_dir, f"{self.name}.csv"))
        return all_table

    def _generate_id(self):
        return self.name



                    
