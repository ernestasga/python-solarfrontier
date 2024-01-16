"API to comunicate with the inverter."

import logging

import aiohttp

from .const import (
    PATH_SYSTEM_INFO,
    PATH_MEASUREMENTS,
    PATH_YIELD_DAY,
    PATH_YIELD_MONTH,
    PATH_YIELD_YEAR,
    PATH_YIELD_TOTAL
)
from .utils import SolarFrontierWebInfoParser

_LOGGER = logging.getLogger(__name__)

class SolarFrontierAPI:
    def __init__(self, host: str) -> None:
        """Initialize the API object."""
        self.host = host
        if not self.host.startswith(('http://', 'https://')):
            self.host = f"http://{self.host}"
        self._session = None

    @property
    def session(self):
        """Lazy initialization of the aiohttp.ClientSession."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def test_connection(self) -> bool:
        """Test if we can connect with the host."""
        try:
            system_info = await self.get_system_info()
            return system_info.get('model_name') is not None
        except aiohttp.ClientError:
            return False

    async def get_system_info(self) -> dict:
        """Get system information from the inverter."""
        try:
            async with self.session.get(f"{self.host}{PATH_SYSTEM_INFO}", timeout=5) as response:
                if response.status == 200:
                    parser = SolarFrontierWebInfoParser()
                    return parser.parse_system_info(await response.text())
        except aiohttp.ClientError:
            return {}

    async def get_measurements(self) -> dict:
        """Get measurement data from the inverter."""
        try:
            async with self.session.get(f"{self.host}{PATH_MEASUREMENTS}", timeout=5) as response:
                if response.status == 200:
                    parser = SolarFrontierWebInfoParser()
                    return parser.parse_measurements(await response.text())
        except aiohttp.ClientError:
            return {}

    async def get_yield_day(self) -> float:
        """Get the yield of the current day."""
        try:
            async with self.session.get(f"{self.host}{PATH_YIELD_DAY}", timeout=5) as response:
                if response.status == 200:
                    parser = SolarFrontierWebInfoParser()
                    return parser.parse_yield(await response.text())
        except aiohttp.ClientError:
            return 0.0

    async def get_yield_month(self) -> float:
        """Get the yield of the current month."""
        try:
            async with self.session.get(f"{self.host}{PATH_YIELD_MONTH}", timeout=5) as response:
                if response.status == 200:
                    parser = SolarFrontierWebInfoParser()
                    return parser.parse_yield(await response.text())
        except Exception:
            return 0.0

    async def get_yield_year(self) -> float:
        """Get the yield of the current year."""
        try:
            async with self.session.get(f"{self.host}{PATH_YIELD_YEAR}", timeout=5) as response:
                if response.status == 200:
                    parser = SolarFrontierWebInfoParser()
                    return parser.parse_yield(await response.text())
        except aiohttp.ClientError:
            return 0.0

    async def get_yield_total(self) -> float:
        """Get the total yield."""
        try:
            async with self.session.get(f"{self.host}{PATH_YIELD_TOTAL}", timeout=5) as response:
                if response.status == 200:
                    parser = SolarFrontierWebInfoParser()
                    return parser.parse_yield(await response.text())
        except aiohttp.ClientError:
            return 0.0

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
