"""The Commodity class represents a commodity in the ranking system."""
import unittest


class Commodity:
    """The Commodity class."""
    def __init__(self, name, value, depreciation_rate=0.0, quantity=0.0):
        """Initialize the commodity."""
        self._depreciation_rate = depreciation_rate
        self._value = value
        self.name = name
        self.quantity = quantity

    def depreciate(self):
        """Depreciate the quantity by the depreciation rate."""
        self.quantity = self.quantity * (1.0 - self._depreciation_rate)

    def total_value(self):
        """The total value of this commodity.

        :return: The quantity times the value.
        """
        return self.quantity * self._value


class TestCommodity(unittest.TestCase):
    """Unit test class to test the Commodity class functions."""

    def test_depreciate(self):
        """Test the depreciate function."""
        quantity = 4
        depreciation_rate = 0.1
        commodity = Commodity("commodity-1", 1, depreciation_rate, quantity)
        commodity.depreciate()
        self.assertEqual(commodity.quantity,
                         quantity * (1.0 - depreciation_rate),
                         "Commodity quantity not correct.")

    def test_total_value(self):
        """Test the total value function."""
        quantity = 0.4
        value = 2
        commodity = Commodity("commodity-1", value, quantity=quantity)
        self.assertEqual(commodity.total_value(), quantity * value)
