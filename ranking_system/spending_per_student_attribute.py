"""The Attribute class represents a purchasable attribute
   in the ranking system."""
import logging
from ranking_system import Attribute

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


LOGGER = logging.getLogger('ranking_system.spending_per_student_attribute')


def _production_function(funding_allocated, production_efficiency):
    """The production function for this attribute.

    :param funding_allocated: Funds allocated to producing the attribute.
    :param production_efficiency: Percent efficiency between [0, 1).
    :return: The amount of the attribute produced given the funds allocated.
    """

    LOGGER.debug('funding_allocated = %f', funding_allocated)
    LOGGER.debug('production_efficiency = %f', production_efficiency)

    # Educational: spending on instruction, research, and student services
    # Non-educational: spending on sports, dorms, and hospitals
    # Universities will differ in the percentage of dollars spent on educational
    # versus non-educational resources.
    # The educational spending percentage may change from year to year.
    educational_spending_percentage = production_efficiency
    amount_produced = funding_allocated * educational_spending_percentage

    LOGGER.debug('amount_produced = %f', amount_produced)

    return amount_produced


def _valuation_function(average_spending_per_student):
    """Valuation given to the average spending per student attribute.

    :param average_spending_per_student: The value used to obtain the valuation.
    :return: The valuation function applied to the value.
    """

    LOGGER.debug('average_spending_per_student = %f',
                 average_spending_per_student)

    # Step like function for average spending per student
    if average_spending_per_student > 10_000:
        # Spending more than 10,000 per student receives the most credit
        valuation = 100
    elif average_spending_per_student > 7_500:
        # Spending between 7,500 and 10,000 per student scores second highest
        valuation = 75
    elif average_spending_per_student > 5_000:
        # Spending between 5,000 and 7,500 per student scores third highest
        valuation = 50
    elif average_spending_per_student > 2_500:
        # Spending between 2,500 and 5,000 per student scores fourth highest
        valuation = 25
    else:
        # Spending less than 2,500 per student receives no credit
        valuation = 0

    LOGGER.debug('valuation = %f', valuation)

    return valuation


def _weightage_function(time_step):
    """Weight given to this attribute based on the current time step.

    :param time_step: The current time step.
    :return: The weightage for this attribute at this time step.
    """

    LOGGER.debug('time_step = %f', time_step)

    # Decreases at time t greater than 5.
    if time_step < 5:
        weight = 0.7
    else:
        weight = 0.6

    LOGGER.debug('weight = %f', weight)

    return weight


class SpendingPerStudentAttribute(Attribute):
    """The Average Spending Per Student Attribute class."""

    def __init__(self):
        """Initialize the attribute."""

        super().__init__('Average Spending Per Student', _weightage_function,
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
