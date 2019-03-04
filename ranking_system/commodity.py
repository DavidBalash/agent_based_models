"""The Commodity class represents a commodity in the ranking system."""

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


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
