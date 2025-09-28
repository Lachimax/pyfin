from pyfin.contained import Contained
from pyfin.portfolio import Portfolio
# from .product import ETFProduct

class ETFUnit(Contained):
    params = {
        "product": None,
        "purchased": None,
    }
    date_keys = ["purchased"]
    _container_key = "portfolio"
    container_class = Portfolio
    def __init__(
            self, 
            path = None, 
            **kwargs
        ):
        super().__init__(path, **kwargs)
        if self.product is None:
            raise ValueError("No product declared for ETFUnit")

    def purchased_for(self):
        return self.product.value_at_date(self.purchased)

    def maturation(self):
        return self.purchased + self.product.suggested_term

    def value_at_maturation(self):
        return self.product.value_at_date(self.maturation())

    def return_at_maturation(self):
        return self.value_at_maturation() - self.purchased_for()

    def _generate_id(self, n):
        return f"{self.product.code}_{self.purchased}_{n}"
        
