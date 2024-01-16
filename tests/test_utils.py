import unittest
from python_solarfrontier.utils import SolarFrontierWebInfoParser, UnitConverter


class TestSolarFrontierWebInfoParser(unittest.TestCase):

    def test_parse_system_info_valid(self):
        html_content = "<td>Name</td><td>SF1234</td><td>Nominal Power</td><td>5.0 kW</td>"
        expected = {"model_name": "SF1234", "nominal_power": "5.0 kW"}
        result = SolarFrontierWebInfoParser.parse_system_info(html_content)
        self.assertEqual(result, expected)

    def test_parse_system_info_invalid(self):
        html_content = "<div>Some unrelated content</div>"
        result = SolarFrontierWebInfoParser.parse_system_info(html_content)
        self.assertEqual(result, {})

    def test_parse_measurements_valid(self):
        html_content = "<tr><td>P DC</td><td align='right'>5.0</td><td>W</td></tr>"
        expected = {"dc_power": "5.0W"}
        result = SolarFrontierWebInfoParser.parse_measurements(html_content)
        self.assertEqual(result, expected)

    def test_parse_measurements_invalid(self):
        html_content = "<div>Invalid content</div>"
        result = SolarFrontierWebInfoParser.parse_measurements(html_content)
        self.assertEqual(result, {})

    def test_parse_yield_valid(self):
        html_content = 'document.getElementById("labelValueId").innerHTML = "10.5Wh"'
        expected = "10.5Wh"
        result = SolarFrontierWebInfoParser.parse_yield(html_content)
        self.assertEqual(result, expected)

    def test_parse_yield_invalid(self):
        html_content = "<div>Invalid content</div>"
        result = SolarFrontierWebInfoParser.parse_yield(html_content)
        self.assertIsNone(result)
        
class TestUnitConverter(unittest.TestCase):

    def setUp(self):
        self.converter = UnitConverter()

    def test_parse_measurement_valid(self):
        test_cases = [
            ("10W", (10.0, "W")),
            ("5.5kW", (5.5, "kW")),
            ("3.2MWh", (3.2, "MWh"))
        ]
        for measurement, expected in test_cases:
            with self.subTest(measurement=measurement):
                self.assertEqual(self.converter.parse_measurement(measurement), expected)

    def test_parse_measurement_invalid(self):
        invalid_measurements = ["10", "kW", "abc"]
        for measurement in invalid_measurements:
            with self.subTest(measurement=measurement):
                with self.assertRaises(ValueError):
                    self.converter.parse_measurement(measurement)

    def test_get_value(self):
        self.assertEqual(self.converter.get_value("15.5kW"), 15.5)

    def test_get_unit(self):
        self.assertEqual(self.converter.get_unit("200Wh"), "Wh")

    def test_parse_measurement_with_spaces(self):
        self.assertEqual(self.converter.parse_measurement("10 kW"), (10.0, "kW"))

    # Additional tests for get_value
    def test_get_value_varied_formats(self):
        test_cases = [("1000kW", 1000.0), ("0.0001MW", 0.0001)]
        for measurement, expected in test_cases:
            with self.subTest(measurement=measurement):
                self.assertEqual(self.converter.get_value(measurement), expected)

    # Additional tests for get_unit
    def test_get_unit_various_formats(self):
        test_cases = [("1000kw", "kw"), ("1000Kw", "Kw"), ("1megawatt", "megawatt")]
        for measurement, expected in test_cases:
            with self.subTest(measurement=measurement):
                self.assertEqual(self.converter.get_unit(measurement), expected)

if __name__ == '__main__':
    unittest.main()
