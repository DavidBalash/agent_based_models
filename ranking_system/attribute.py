"""The Attribute class represents a purchasable attribute
   in the ranking system."""

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


class Attribute:
    """The Attribute class."""
    def __init__(self, name, ranking_weight, initial_quantity=0.0):
        """Initialize the attribute.

        :param name: The name of the attribute.
        :param ranking_weight: The weight used in the ranking process.
        :param initial_quantity: The initial quantity. (default 0.0)
        """

        self.name = name
        self._ranking_weight = ranking_weight
        self._quantity = initial_quantity

    def set_quantity(self, quantity):
        """Set the quantity of the attribute.

        :param quantity: The quantity to set.
        """

        self._quantity = quantity

    def simple_production_function(self, capital, alpha):
        """The simple production function for this attribute.

        :param capital: The input capital.
        :param alpha: The input elasticity alpha.
        """

        self._quantity += capital ** alpha

    # pylint: disable=too-many-arguments
    def cobb_douglas_production_function(self, total_factor_productivity,
                                         labor, capital, alpha, beta):
        """The Cobb-Douglas production function for this attribute.

        :param total_factor_productivity: The total-factor productivity (TFP).
        :param labor: The input labor.
        :param capital: The input capital.
        :param alpha: The input elasticity alpha.
        :param beta: The input elasticity beta.
        """

        self._quantity += (total_factor_productivity
                           * (labor ** beta)
                           * (capital ** alpha))

    def valuation(self):
        """The value of this attribute in the ranking."""

        return self._quantity * self._ranking_weight

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
