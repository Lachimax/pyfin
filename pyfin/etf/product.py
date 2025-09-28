import numpy as np

from astropy import units as u
from astropy import time as t

from pyfin.simulated import Simulated
from .unit import ETFUnit
from pyfin.portfolio import Portfolio


class ETFProduct(Simulated):
    params = {
        "code": "",
        "provider": "Vanguard",
        "suggested_term": 3 * u.yr,
        "predicted_annual_growth": 0.06,
        "starting_value": 0.,
        "start_date": t.Time("2025-09-25")
    }
    date_keys = ["start_date"]
    container_class = Portfolio
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.value: float = self.starting_value * 1.
        self.record[self.start_date] = {"value": self.starting_value}

    def generate_id(self, **kwargs):
        return self.code

    def value_at_date(self, date: t.Time):
        recorded_dates = list(sorted(self.record.keys(), key=lambda k: date - k))
        closest = recorded_dates[0]
        if len(recorded_dates) > 1:
            second_closest = recorded_dates[1]
            latest = max(closest, second_closest)
            sandwiched = date < latest
        else:
            latest = closest
            sandwiched = False
        if sandwiched:
            return self.record[closest]["value"] # TODO: Maybe interpolate
        else:
            delta = date - latest
            delta = delta.to(u.yr)
            last_value = self.record[latest]["value"]
            return last_value * (1. + self.predicted_annual_growth) ** delta.value

    def step(
            self,
            step_size: u.Quantity = 1 * u.fortnight,
            date: u.Quantity = None,
    ):
        step_props = super().step(step_size)
        growth_factor = self.predicted_annual_growth / self.container.steps_per_year
        delta = np.round((self.value * growth_factor).decompose(), 2)
        old_value = self.value
        self.value = np.round(self.value + delta, 2)
        self.message(f"\t{self.id}: Value changes by {delta}, {old_value} -> {self.value}")
        step_props["value"] = self.value
        step_props["value_change"] = delta
        self.record[step_props["date"]] = step_props
        return step_props

    def new_unit(self, purchased: t.Time):
        unit = ETFUnit(product=self, purchased=purchased, container=self.container)
        self.container.add_item(unit)
        return unit
