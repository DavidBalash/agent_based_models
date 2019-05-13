"""The Attribute class represents a purchasable attribute
   in the ranking system."""
import logging
import numpy as np
from ranking_system import Attribute

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


LOGGER = logging.getLogger('ranking_system.class_size_attribute')


def _production_function(funding_allocated, production_efficiency):
    """The production function for this attribute.

    :param funding_allocated: Funds allocated to producing the attribute.
    :param production_efficiency: Percent efficiency between [0, 1).
    :return: The amount of the attribute produced given the funds allocated.
    """

    LOGGER.debug('funding_allocated = %f', funding_allocated)
    LOGGER.debug('production_efficiency = %f', production_efficiency)

    max_value = 15_000
    steepness = 3 * production_efficiency
    amount_produced = 200 - (200 * np.tanh(np.interp(funding_allocated,
                                                     [0, max_value],
                                                     [0, steepness])))

    LOGGER.debug('amount_produced = %f', amount_produced)

    return amount_produced


def _valuation_function(average_class_size):
    """Valuation given to the average class size attribute.

    :param average_class_size: The value on which to obtain the valuation.
    :return: The valuation function applied to the value.
    """

    LOGGER.debug('average_class_size = %f', average_class_size)

    # Step like function for average class size
    if average_class_size < 20:
        # Classes with fewer than 20 students receive the most credit
        valuation = 100
    elif average_class_size < 30:
        # Classes with 20 to 29 students score second highest
        valuation = 75
    elif average_class_size < 40:
        # Classes with 30 to 39 students score third highest
        valuation = 50
    elif average_class_size < 50:
        # Classes with 40 to 49 students score fourth highest
        valuation = 25
    else:
        # Classes that are 50 or more students receive no credit
        valuation = 0

    LOGGER.debug('valuation = %f', valuation)

    return valuation


def _weightage_function(time_step):
    """Weight given to average class size attribute.

    :param time_step: The current time step.
    :return: The weightage for this attribute at this time step.
    """

    LOGGER.debug('time_step = %f', time_step)

    # Increases at time t greater than 5.
    if time_step < 5:
        weight = 0.3
    else:
        weight = 0.4

    LOGGER.debug('weight = %f', weight)

    return weight


class ClassSizeAttribute(Attribute):
    """The Average Class Size Attribute class."""

    def __init__(self):
        """Initialize the attribute."""

        super().__init__('Average Class Size', _weightage_function,
                         _valuation_function, _production_function)

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
