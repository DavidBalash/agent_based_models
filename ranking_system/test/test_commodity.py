"""Unit test for the Commodity class."""
from commodity import Commodity
import unittest

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


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


if __name__ == '__main__':
    unittest.main()

# Agent based models
# Copyright (C) 2019 David Balash
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
