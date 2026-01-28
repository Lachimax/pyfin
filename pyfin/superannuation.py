from astropy import units as u

from .account import Account

class Superannuation(Account):
    def step(
            self,
            step_size: u.Quantity = 1 * u.day,
    ):
        step_props = super().step(step_size=step_size)

        self.record[step_props["date"]] = step_props
        return step_props

