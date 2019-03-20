"""The Attribute class represents a purchasable attribute
   in the ranking system."""
import logging

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


LOGGER = logging.getLogger('ranking_system.attribute')


class Attribute:
    """The Attribute class."""
    def __init__(self, name, weightage_function, valuation_function,
                 production_function):
        """Initialize the attribute.

        :param name: The name of the attribute.
        :param weightage_function: Function used to provide the ranking weight.
        :param valuation_function: Function used to provide a valuation.
        :param production_function: Function used to produce the attribute.
        """

        LOGGER.debug('name = %s', name)
        LOGGER.debug('weightage_function = %s', weightage_function.__name__)
        LOGGER.debug('valuation_function = %s', valuation_function.__name__)
        LOGGER.debug('production_function = %s', production_function.__name__)

        self.name = name
        self.value = 0
        self._valuation_function = valuation_function
        self._weightage_function = weightage_function
        self._production_function = production_function

    def production(self, funding_allocated, production_efficiency):
        """The production function for this attribute.

        :param funding_allocated: Funds allocated to producing the attribute.
        :param production_efficiency: Percent efficiency between [0, 1).
        :return: The amount of the attribute produced given the funds allocated.
        """

        LOGGER.debug('funding_allocated = %f', funding_allocated)
        LOGGER.debug('production_efficiency = %f', production_efficiency)
        amount_produced = self._production_function(funding_allocated,
                                                    production_efficiency)
        LOGGER.debug('amount_produced = %f', amount_produced)
        return amount_produced

    def valuation(self, value):
        """The true value of this attribute.

        :param value: The value on which to obtain the valuation.
        :return: The valuation function applied to the value.
        """

        LOGGER.debug('value = %f', value)
        valuation = self._valuation_function(value)
        LOGGER.debug('valuation = %f', valuation)
        return valuation

    def weightage(self, time_step):
        """The weight given to this attribute in the ranking at this time step.

        :param time_step: The current time step.
        :return: The weightage for this attribute at this time step.
        """

        LOGGER.debug('time_step = %f', time_step)
        weight = self._weightage_function(time_step)
        LOGGER.debug('weight = %f', weight)
        return weight

    def __repr__(self):
        """The representation function will return the string representation.

        :return: The string representation of the Attribute class.
        """

        return 'Attribute[name={}, value={}]'.format(self.name, self.value)


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
