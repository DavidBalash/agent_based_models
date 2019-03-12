"""Unit test for the Attribute class."""
import unittest
from attribute import Attribute

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


# pylint: disable=protected-access
class TestAttribute(unittest.TestCase):
    """Unit test class to test the Attribute class functions."""

    def test_simple_production_function(self):
        """Test the simple production function."""
        capital = 4
        alpha = 0.5
        attribute = Attribute("attribute-1", 0.5)
        attribute.simple_production_function(capital, alpha)
        self.assertEqual(attribute._quantity, capital ** alpha,
                         "Attribute quantity not correct.")

    def test_cobb_douglas_production_function(self):
        """Test the simple production function."""
        capital = 4
        labor = 9
        alpha = 0.5
        beta = 0.5
        tfp = 1
        ranking_weight = 0.5
        attribute = Attribute("attribute-1", ranking_weight)
        attribute.cobb_douglas_production_function(tfp, labor, capital, alpha, beta)
        self.assertEqual(attribute._quantity,
                         tfp * (labor ** beta) * (capital ** alpha),
                         "Attribute quantity not correct.")

    def test_ranking_value(self):
        initial_quantity = 10
        ranking_weight = 0.5
        attribute = Attribute("attribute-1", ranking_weight, initial_quantity)
        self.assertEqual(attribute.valuation(),
                         initial_quantity * ranking_weight,
                         "Ranking value not correct.")


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
