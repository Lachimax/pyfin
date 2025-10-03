from pyfin.contained import Contained

class ETFUnit(Contained):
    params = {
        "product": None,
        "purchased": None,
        "price": None
    }
    date_keys = ["purchased"]
    money_keys = ["price"]
    _container_key = "product"
    def __init__(
            self, 
            path = None, 
            **kwargs
        ):
        super().__init__(path, **kwargs)
        if self.product is None:
            raise ValueError("No product declared for ETFUnit")

    def purchased_for(self):
        if self.price is None:
            price = self.product.value_at_date(self.purchased)
        else:
            price = self.price
        return price

    def maturation(self):
        return self.purchased + self.product.suggested_term

    def value_at_maturation(self):
        return self.product.value_at_date(self.maturation())

    def return_at_maturation(self):
        return self.value_at_maturation() - self.purchased_for()

    def _generate_id(self, n):
        return f"{self.product.code}_{self.purchased}_{n}"
        
    @classmethod
    def _container_class(cls):
        from pyfin.portfolio import Portfolio
        return Portfolio