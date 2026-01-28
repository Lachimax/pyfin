from astropy import units as u
from astropy import time as t

from .utils import dollar
from .simulated import Simulated

class Appreciable(Simulated):
    params = {
        "starting_value": 0. * dollar,
        # Per annum
        "appreciation_rate": 0.,
        "start_date": t.Time.now(),
    }

    def __init__(self, path, **kwargs):
        super().__init__(path=path, kwargs=kwargs)
        self.value: float = self.starting_value * 1.
        self.record[self.start_date] = {"value": self.starting_value}

    def appreciate(
            self,
            delta_time: u.Quantity,
            initial_value: float = None
    ):
        if initial_value is None:
            initial_value = self.value
        # Calculate growth
        new_value = initial_value * (1 + self.appreciation_rate) ** (delta_time / u.yr)
        return new_value