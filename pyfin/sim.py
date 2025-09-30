import astropy.units as u

import astropy.time as t

from .container import Container
from .simulated import Simulated
from .utils import relevant_timescale


class Simulation(Container):
    def __init__(self, path=None, **kwargs):
        super().__init__(path, **kwargs)
        self.step_size = 1 * u.fortnight
        self.date: t.Time = None
        self.start_date: t.Time = None
        self.end_date: t.Time = None
        self.steps_per_year: float = self._steps_per_year()
        self.output_dir: str = None
        self.input_dir: str = None

    def simulate(
            self,
            start_date: t.Time = None,
            end_date: t.Time = None,
            length: u.Quantity = 50 * u.yr,
            step_size: u.Quantity = None,
            verbose: bool = None,
    ):
        if step_size is not None:
            self.step_size = step_size
        if verbose is not None:
            self.verbose = verbose
        if start_date is None:
            start_date = t.Time.now()
        self.start_date = start_date
        if end_date is None:
            if length is None:
                raise ValueError(f"Either length or end_date must be specified.")
            else:
                end_date = start_date + length
        self.end_date = end_date
        self.steps_per_year = self._steps_per_year()
        n = 0
        self.date = self.start_date.copy()
        while self.date < end_date:
            elapsed = (self.date - self.start_date).to(u.s)
            self.message(f"{n}: {self.date}, {relevant_timescale(elapsed)} elapsed.")
            self.step()
            n += 1
            self.date += self.step_size

    def _steps_per_year(self):
        return u.yr / self.step_size

    def step(self):
        for idn, obj in self._registry.items():
            if isinstance(obj, Simulated):
                obj.step()