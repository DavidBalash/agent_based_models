"""Unit test for the Good class."""
import unittest
from good import Good

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


# pylint: disable=protected-access
class TestGood(unittest.TestCase):
    """Unit test class to test the Good class functions."""

    def test_simple_production_function(self):
        """Test the simple production function."""
        capital = 4
        alpha = 0.5
        good = Good("good-1", 0.5)
        good.simple_production_function(capital, alpha)
        self.assertEqual(good._quantity, capital ** alpha,
                         "Good quantity not correct.")

    def test_cobb_douglas_production_function(self):
        """Test the simple production function."""
        capital = 4
        labor = 9
        alpha = 0.5
        beta = 0.5
        tfp = 1
        ranking_weight = 0.5
        good = Good("good-1", ranking_weight)
        good.cobb_douglas_production_function(tfp, labor, capital, alpha, beta)
        self.assertEqual(good._quantity,
                         tfp * (labor ** beta) * (capital ** alpha),
                         "Good quantity not correct.")

    def test_ranking_value(self):
        initial_quantity = 10
        ranking_weight = 0.5
        good = Good("good-1", ranking_weight, initial_quantity)
        self.assertEqual(good.ranking_value(),
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
