import os

from astropy import units, time

from .sim import Simulation
from pyfin.etf.product import ETFProduct

class Portfolio(Simulation):
    def load_etfs(self):
        product_directory = os.path.join(self.input_dir, "etf", "products")
        product_files = os.listdir(product_directory)
        for file in product_files:
            path = os.path.join(product_directory, )