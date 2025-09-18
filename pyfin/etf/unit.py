from pyfin.generic import Generic
from pyfin.contained import Contained
from .product import ETFProduct

class ETFUnit(Contained):
    params = {
        "product": None,
        "purchased": None,
    }
    _container_key = "portfolio"
    def __init__(
            self, 
            path = None, 
            **kwargs
        ):
        super().__init__(path, **kwargs)
        if self.product is None:
            raise ValueError("No product declared for ETFUnit")