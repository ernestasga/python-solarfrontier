# Solar Frontier Inverter API

<div align="center">

  <img src="https://github.com/ernestasga/python-solarfrontier/tree/main/images/solar-frontier-logo.png" alt="solar-frontier-logo" >

  <a href="https://github.com/ernestasga/python-solarfrontier/actions/workflows/test.yml">
    <img src="https://github.com/ernestasga/python-solarfrontier/actions/workflows/test.yml/badge.svg" alt="Tests">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Version">
  <a href="https://pypi.org/project/python-solarfrontier/">
    <img src="https://img.shields.io/pypi/v/python-solarfrontier.svg" alt="PyPI Version">
  </a>

</div>
<p align="center">
  Python Library to retrieve data from "Solar Frontier" inverters on LAN. Able to get measurements, yield data, system info.
</p>


# Installation
Available on PyPi
```bash
pip install python-solarfrontier
```

# Compatibility
**Confirmed to work with:**

* SF-WR-5503x

# Example
Initiate the API instance with host. Authentication not supported.

```
import asyncio

from python_solarfrontier.api import SolarFrontierAPI
from python_solarfrontier.utils import UnitConverter

async def main():
    host = '192.168.0.101' # IP address of the inverter
    api = SolarFrontierAPI(host)

    # Test if we can connect with the host
    test = await api.test_connection()
    print(f"Test connection: {test}")

    # Get system information
    system_info = await api.get_system_info()
    print(f"System information: {system_info}")

    # Get measurement data
    measurements = await api.get_measurements()
    print(f"Measurement data: {measurements}")

    # Get the yield of the current day
    yield_day = await api.get_yield_day()
    print(f"Yield of the current day: {yield_day}")

    # Get the yield of the current month
    yield_month = await api.get_yield_month()
    print(f"Yield of the current month: {yield_month}")

    # Get the yield of the current year
    yield_year = await api.get_yield_year()
    print(f"Yield of the current year: {yield_year}")

    #Get total yield
    yield_total = await api.get_yield_total()
    print(f"Total yield: {yield_total}")

    # Close the session
    await api.close()


    # Get measurement values and units
    unit_converter = UnitConverter()
    total_yield_value, total_yield_unit = unit_converter.parse_measurement(yield_total)
    print(f"Total yield value: {total_yield_value}, unit: {total_yield_unit}")

# Run the async main function
asyncio.run(main())
```

# Contribution
Feel free to contribute with PR to `dev` brach.