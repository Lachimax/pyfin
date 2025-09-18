import pyfin.utils as u
from astropy import units
from pyfin.generic import Generic

class ETFProduct(Generic):
    params = {
        "code": "",
        "provider": "Vanguard",
        "suggested_term": 3 * units.yr,
        "predicted_annual_growth": 0.06
    }

    def generate_id(self, **kwargs):
        return self.code