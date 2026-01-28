from __future__ import annotations
from typing import TYPE_CHECKING

import os

from astropy import units, time
from astropy.table import QTable

from .sim import Simulation
from .etf.product import ETFProduct
from .etf.unit import ETFUnit
from . import utils
if TYPE_CHECKING:
    from .container import Container

class Portfolio(Simulation):
    """The Portfolio actually contains only products, which themselves contain the units that make up a portfolio.
    """
    def __init__(self, path=None, **kwargs):
        super().__init__(path, **kwargs)
        self.product_directory = os.path.join(self.input_dir, "etf", "products")
        self.unit_directory = os.path.join(self.input_dir, "etf", "units")
        self.invested = 0. * utils.dollar
        self.value = 0. * utils.dollar

        
    def load_etfs(self):
        for file in sorted(os.listdir(self.product_directory)):
            path = os.path.join(self.product_directory, file)
            if os.path.isfile(path) and "template" not in file:
                self.message("Loading ETF Product from", path)
                etf_product = ETFProduct.from_file(path)
                self.add_item(etf_product)
        for product_name in os.listdir(self.unit_directory): # Directories containing unit files
            directory = os.path.join(self.unit_directory, product_name)
            self.message("Product units for", product_name, "from", directory)
            for file in sorted(os.listdir(directory)): # Unit files
                path = os.path.join(directory, file)
                if os.path.isfile(path) and "template" not in file:
                    self.message("\tLoading ETF Unit from", path)
                    etf_product = self[product_name]
                    etf_unit = ETFUnit.from_file(path, container=etf_product)
                    etf_product.add_item(etf_unit)

        print()

    def returns(self):
        return self.value - self.invested

    def write_etfs(self):
        for key, product in self._registry.items():
            for idn, unit in product._registry.items():
                unit.to_file()

    def print_etfs(self):
        for name, product in self._registry.items():
            print("=" * 20)
            print(name)
            product.print_items()
            print()

    def add_etf_units_csv(self, path: str, skip_existing: bool = True):
        """Import ETF purchases from a Vanguard transactions CSV.

        Args:
            path (str): Path of file.
        """
        
        tbl = QTable.read(path, format="csv")
        added = []
        for row in tbl:
            print("\n", row)
            product_name = row["Product ID"]
            if product_name not in self._registry:
                raise ValueError(f"Product {product_name} not found in portfolio.")
            
            n = int(row["Quantity"])
            product = self[product_name]
            purchased = time.Time.strptime(row["Trade Date"], r"%d-%b-%Y")
            price = float(row["Unit Price"])
            
            # Check for duplicates
            if skip_existing:
                matching = product.check_for_unit(purchased)
                if len(matching) >= n:
                    print(f"Skipping {n} units of {product_name} purchased on {purchased.strftime('%Y-%m-%d')} as {len(matching)} already exist.")
            
                n = n - len(matching)
            
            for i in range(n):
                etf_unit = ETFUnit(
                    container=product,
                    purchased=purchased,
                    price=price * utils.dollar
                )
                product.add_item(etf_unit)
                added.append(etf_unit.id)
                print(f"\tAdded {product_name} unit {i + 1} of {n} ({etf_unit.id})")
                
        added.sort()
        print(f"\nAdded {len(added)} ETF units:")
        for p in added:
            print(p)


    def add_etf_units_ui(self):
        self.print_etfs()
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
                added.append(etf_unit.id)
            added.sort()
            print(f"Added {len(added)} ETF units:")
            for p in added:
                print(p)
            # for key, product in self._registry.items():
            #     for item in product._registry:
            #         print(item)
            cont = utils.select_yn("Were other products purchased in this transaction?")

    def update_etf_values_ui(self):
        for name, product in self._registry.items():
            if utils.select_yn(f"Update value for product {name}?"):
                new_value = utils.user_input(
                    message=f"Enter new value for unit {name} (currently {product.value.round(2)}):",
                    input_type=float
                )
                product.value = new_value * utils.dollar
                product.add_record(date=time.Time.now(), value=product.value)
                print(f"\tUpdated value to {product.value.round(2)}")
                # product.to_file()

    def collect_dicts(self):
        dicts = []
        for name, product in self._registry.items():
            dicts += product.collect_dicts()
        return dicts

    def tabulate(self):
        all_table = QTable(self.collect_dicts())
        all_table.remove_column("verbose")
        all_table.sort("id")
        self.invested = all_table["price"].sum()
        self.value = all_table["present_value"].sum()
        print("Total invested:", self.invested)
        print("Total present value:", self.value)
        print("Total present return:", self.returns())
        if isinstance(self.input_dir, str):
            all_table.write(os.path.join(self.input_dir, f"{self.name}.ecsv"), overwrite=True)
            all_table.write(os.path.join(self.input_dir, f"{self.name}.csv"), overwrite=True)



        return all_table

    def _generate_id(self):
        return self.name



                    
