import astropy.units as u

from .contained import Contained

class Simulated(Contained):
    def __init__(self, path = None, **kwargs):
        self.record: dict = {}
        super().__init__(path, **kwargs)

    def step(
            self,
            step_size: u.Quantity = 1 * u.fortnight,
            date: u.Quantity = None,
    ):
        step_props = {}
        if self.container is None:
            raise ValueError(f"{self.id} has no simulation container.")
        step_props["step_size"] = self.container.step_size
        step_props["date"] = self.container.date
        self.record[step_props["date"]] = step_props
        return step_props


