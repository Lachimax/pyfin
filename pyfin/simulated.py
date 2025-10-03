import astropy.units as u
import astropy.time as t

from .contained import Contained

class Simulated(Contained):
    def __init__(self, path = None, **kwargs):
        self.record: dict = {}
        super().__init__(path, **kwargs)
        self._record_from_yaml()

    def step(
            self,
            step_size: u.Quantity = 1 * u.day,
    ):
        step_props = {}
        if self.container is None:
            raise ValueError(f"{self.id} has no simulation container.")
        step_props["step_size"] = self.container.step_size
        step_props["date"] = self.container.date
        self.record[step_props["date"]] = step_props
        return step_props

    def _record_for_yaml(self):
        _record = {}
        for key, value in self.record.items():
            _record[str(key)] = value
        return _record

    def _record_from_yaml(self):
        _record = {}
        for key, value in self.record.items():
            _record[t.Time(key)] = value
        self.record = _record
        return self.record

    def to_dict(self):
        dictionary = super().to_dict()
        dictionary["record"] = self._record_for_yaml()
        return dictionary

