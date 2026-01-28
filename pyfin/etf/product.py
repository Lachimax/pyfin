import os

from astropy import units as u
from astropy import time as t

from ..appreciable import Appreciable
from ..container import Container


class ETFProduct(Appreciable, Container):
    params = Appreciable.params.update(
        {
            "code": "",
            "provider": "Vanguard",
            "suggested_term": 3 * u.yr,
            "management_fee": 0.0027
        }
    )
    _container_key = "portfolio"
    date_keys = ["start_date"]
    money_keys = ["starting_value"]

    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)


    def generate_id(self, **kwargs):
        return self.code

    def check_for_unit(self, purchased: t.Time):
        matching = []
        for idn, unit in self._registry.items():
            if unit.purchased == purchased:
                matching.append(unit)
        return matching

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
            return self.record[closest]["value"]  # TODO: Maybe interpolate
        else:
            delta = date - latest
            delta = delta.to(u.yr)
            last_value = self.record[latest]["value"]
            new_value, _ = self.appreciate(delta_time=delta, initial_value=last_value)
            return new_value

    def appreciate(
            self,
            delta_time: u.Quantity,
            initial_value: float = None
    ):
        new_value = super().appreciate(delta_time=delta_time, initial_value=initial_value)
        # Calculate management fee
        fee = ((1 - self.management_fee) ** (delta_time / u.yr) - 1) * new_value
        new_value = new_value - fee
        return new_value, fee

    def step(
            self,
            step_size: u.Quantity = 1 * u.fortnight,
    ):
        step_props = super().step(step_size=step_size)
        new_value, fee = self.appreciate(delta_time=step_size)
        old_value = self.value * 1.
        self.value = new_value
        # print(new_value, old_value)
        delta_value = new_value - old_value
        self.message(
            f"\t{self.id}: Value changes by {delta_value} (fees {fee}), {old_value.round(2)} -> {self.value.round(2)}")
        step_props["value"] = self.value
        step_props["value_change"] = delta_value
        date = step_props.pop("date")
        self.add_record(date=date, **step_props)
        return step_props

    def last_record(self):
        last_date = max(self.record.keys())
        return last_date, self.record[last_date]

    def add_record(self, date: t.Time, **kwargs):
        last_date, _ = self.last_record()
        if date > last_date:
            self.value = kwargs["value"]
        self.record[date] = kwargs

    @classmethod
    def _container_class(cls):
        from ..portfolio import Portfolio
        return Portfolio

    def add_item(self, item):
        if item.price is not None and item.purchased is not None:
            self.add_record(date=item.purchased, value=item.price)
        if self.container is not None and isinstance(self.container.path, str):
            item.path = os.path.join(self.container.unit_directory, self.id, item.id + ".yaml")
        super().add_item(item)
