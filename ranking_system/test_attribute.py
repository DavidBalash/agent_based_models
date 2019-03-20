"""Unit test for the Attribute class."""
import unittest
from attribute import Attribute

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


def weightage_function_mock(t):
    """Weightage function mock."""
    return t


def valuation_function_mock(value):
    """Valuation function mock."""
    return value


def production_function_mock(dollars, production_efficiency):
    """Production function mock."""
    return dollars * production_efficiency


# pylint: disable=protected-access
class TestAttribute(unittest.TestCase):
    """Unit test class to test the Attribute class functions."""

    def test_init(self):
        """Test the constructor function."""
        attribute_name = 'Test Attribute'
        attribute = Attribute(attribute_name, weightage_function_mock,
                              valuation_function_mock, production_function_mock)
        self.assertEqual(attribute.name, attribute_name,
                         'Attribute name not correct.')
        self.assertEqual(attribute._weightage_function.__name__,
                         weightage_function_mock.__name__,
                         'Weightage function name not correct.')


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
