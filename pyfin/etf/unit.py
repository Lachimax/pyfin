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
        if self.container is None:
            raise ValueError("No product declared for ETFUnit")

    def purchased_for(self):
        if self.price is None:
            price = self.container.value_at_date(self.purchased)
        else:
            price = self.price
        return price

    def maturation(self):
        return self.purchased + self.container.suggested_term

    def value_at_maturation(self):
        return self.container.value_at_date(self.maturation())

    def return_at_maturation(self):
        return self.value_at_maturation() - self.purchased_for()

    def _generate_id(self, n):
        return f"{self.container.code}_{self.purchased.strftime("%Y-%m-%d")}_{n}"
        
    def to_dict(self):
        dictionary = super().to_dict()
        dictionary.update({
            "maturation_date": self.maturation(),
            "mature_value": self.value_at_maturation(),
            "mature_return": self.return_at_maturation()
        })
        return dictionary

    @classmethod
    def _container_class(cls):
        from pyfin.portfolio import Portfolio
        return Portfolio