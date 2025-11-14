from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .contained import Contained

import astropy.units as u
from astropy.table import QTable

from .generic import Generic


class Container(Generic):

    def __init__(
            self,
            path=None,
            **kwargs
    ):
        self._registry = {}
        super().__init__(path, **kwargs)

    def add_item(self, item: Contained):
        item.set_id()
        self[item.id] = item
        item.container = self

    def check_id(self, idn: str) -> bool:
        """Check object's registry for existing ID.

        Args:
            idn (str): ID

        Returns:
            bool: ID in registry?
        """
        return idn in self._registry

    def list_items(self):
        return list(sorted(self._registry.keys()))

    def collect_dicts(self):
        dicts = []
        for key, item in self._registry.items():
            dictionary = item.to_dict()
            dicts.append(dictionary)
        return dicts

    def print_items(self):
        for item in self.list_items():
            print(item)

    def tabulate(self):
        table = QTable(self.collect_dicts())
        table.sort("id")
        return table

    def __getitem__(self, name):
        return self._registry[name]

    def __setitem__(self, name, value):
        self._registry[name] = value
