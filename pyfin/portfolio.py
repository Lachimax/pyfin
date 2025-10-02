import os

from astropy import units, time

from .sim import Simulation
from pyfin.etf.product import ETFProduct

class Portfolio(Simulation):
    def __init__(self, path=None, **kwargs):
        super().__init__(path, **kwargs)
        
    def load_etfs(self):
        product_directory = os.path.join(self.input_dir, "etf", "products")
        product_files = os.listdir(product_directory)
        for file in product_files:
            path = os.path.join(product_directory, )