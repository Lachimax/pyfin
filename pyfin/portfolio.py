from astropy import units, time

from .container import Container

class Portfolio(Container):
    def simulate(
            self, 
            start_date: time.Time = None,
            end_date: time.Time = None,
            step_size: units.Quantity = 1 * units.fortnight 
        ):
        date = start_date.copy()
        while date < end_date:
            self.step()
            date += step_size
