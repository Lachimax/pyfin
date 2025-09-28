import astropy.units as u

from .container import Container
from .generic import Generic

class Contained(Generic):
    _container_key = "container"
    container_class = Container
    def __init__(self, path = None, **kwargs):
        self.container: Container = None
        super().__init__(path, **kwargs)
        if self.container is None:
            self.container = self.container_class()

    def generate_id(self):
        n = 0
        identifier = self._generate_id(n)
        while self.container.check_id(identifier):
            n += 1
            identifier = self._generate_id(n)
        return identifier

    def _generate_id(self, n):
        return f"{self.name}_{n}"
    
    def to_dict(self):
        dictionary = super().to_dict()
        dictionary[self._container_key] = self.container.id
        dictionary.pop(self._container_key)
        return dictionary
