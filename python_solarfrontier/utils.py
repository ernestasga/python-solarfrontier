"""Utility classes to work with device data."""
import re


class SolarFrontierWebInfoParser:
    """Parser class for Solar Frontier inverter system information."""

    @staticmethod
    def parse_system_info(html_content: str) -> dict:
        """Parse the system information from the inverter's output."""
        info = {}

        # Extract model name
        model_match = re.search(r"<td>Name</td><td>(.*?)</td>", html_content)
        if model_match:
            info["model_name"] = model_match.group(1)

        # Extract nominal power with various unit formats (e.g., W, kW)
        power_match = re.search(r"<td>Nominal Power</td><td>([\d.]+\s?[kM]?W)</td>", html_content)
        if power_match:
            info["nominal_power"] = power_match.group(1)

        return info

    @staticmethod
    def parse_measurements(html_content: str) -> dict:
        """Parse the measurements from the inverter's output."""
        name_mapping = {
            "P DC": "dc_power",
            "U DC": "dc_voltage",
            "I DC": "dc_current",
            "U AC1": "ac_voltage_phase_1",
            "U AC2": "ac_voltage_phase_2",
            "U AC3": "ac_voltage_phase_3",
            "I AC1": "ac_current_phase_1",
            "I AC2": "ac_current_phase_2",
            "I AC3": "ac_current_phase_3",
            "F AC": "ac_frequency",
            "F AC1": "ac_frequency_phase_1",
            "F AC2": "ac_frequency_phase_2",
            "F AC3": "ac_frequency_phase_3",
            "P AC": "ac_power",
            "P AC1": "ac_power_phase_1",
            "P AC2": "ac_power_phase_2",
            "P AC3": "ac_power_phase_3"
        }
        units_data = {}
        table_rows = re.findall(r"<tr><td>(.*?)</td><td align='right'>(.*?)</td><td>(.*?)</td></tr>", html_content)
        for name, value, unit in table_rows:
            key = name_mapping.get(name.strip(), name.strip().replace(" ", "_").lower())
            try:
                numeric_value = float(value.strip())
            except ValueError:
                numeric_value = None
            units_data[key] = f"{numeric_value}{unit.strip()}" if numeric_value is not None else None

        return units_data

    @staticmethod
    def parse_yield(html_content: str) -> str or None:
        """Parse the day yield from the inverter's output."""
        yield_match = re.search(r"document\.getElementById\(\"labelValueId\"\)\.innerHTML\s*=\s*\"[^\"]*?(\d+(\.\d+)?[kM]?Wh)", html_content)
        if yield_match:
            return yield_match.group(1)
        return None


class UnitConverter:
    """Convert measurement units like kW, MWh to base units."""

    def parse_measurement(self, measurement) -> tuple[int, str]:
        """Parse the measurement into value and unit."""
        # value is number or float, rest is unbit
        value_match = re.search(r"^(\d+(\.\d+)?)\s*([a-zA-Z]+)$", measurement.strip())
        if value_match:
            value = float(value_match.group(1))
            unit = value_match.group(3)
            return value, unit
        raise ValueError("Invalid measurement unit")

    def get_value(self, measurement) -> int:
        """Get the value of the measurement."""
        value, _ = self.parse_measurement(measurement.strip())
        return value

    def get_unit(self, measurement) -> str:
        """Get the unit of the measurement."""
        _, unit = self.parse_measurement(measurement.strip())
        return unit
