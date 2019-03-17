"""The Attribute class represents a purchasable attribute
   in the ranking system."""

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


class Attribute:
    """The Attribute class."""
    def __init__(self, name, weightage_function, valuation_function,
                 production_function, initial_value=0.0):
        """Initialize the attribute.

        :param name: The name of the attribute.
        :param weightage_function: The weightage function used in ranking.
        :param valuation_function: The valuation function used in ranking.
        :param production_function: The production function used to produce the
                                    attribute.
        :param initial_value: The initial value. (default 0.0)
        """

        self.name = name
        self._value = initial_value
        self._valuation_function = valuation_function
        self._weightage_function = weightage_function
        self._production_function = production_function

    def production_function(self, dollars, random):
        self._value = self._production_function(dollars, random)

    def valuation(self, time_step):
        """The value of this attribute in the ranking.

        :param time_step: The current time step t.
        """

        return (self._valuation_function(self._value)
                * self._weightage_function(time_step))

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
