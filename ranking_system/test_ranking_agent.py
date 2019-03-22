"""Unit test for the Ranking Agent class."""
import unittest
from ranking_system import Attribute
from ranking_system import RankingAgent
from ranking_system import RankingModel

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


# Create weightage functions that will return the weight used for time t
# The sum of the weightage functions at time t must add up to one

def weightage_average_spending_per_student(t):
    """Weight given to average spending per student attribute
       Decreases at time t greater than 5"""
    return 0.7 if t < 5 else 0.6


def weightage_average_class_size(t):
    """Weight given to average class size attribute
       Increases at time t greater than 5"""
    return 0.3 if t < 5 else 0.4


# Create valuation functions
# Return the true valuation of attribute i at time t

def valuation_average_spending_per_student(average_spending_per_student):
    """Valuation given to the average spending per student attribute"""
    # Step like function for average spending per student
    if average_spending_per_student > 10_000:
        # Spending more than 10,000 per student receives the most credit
        return 100
    elif average_spending_per_student > 7_500:
        # Spending between 7,500 and 10,000 per student scores second highest
        return 75
    elif average_spending_per_student > 5_000:
        # Spending between 5,000 and 7,500 per student scores third highest
        return 50
    elif average_spending_per_student > 2_500:
        # Spending between 2,500 and 5,000 per student scores fourth highest
        return 25
    else:
        # Spending less than 2,500 per student receives no credit
        return 0


def valuation_average_class_size(average_class_size):
    """Valuation given to the average class size attribute"""
    # Step like function for average class size
    if average_class_size < 20:
        # Classes with fewer than 20 students receive the most credit
        return 100
    elif average_class_size < 30:
        # Classes with 20 to 29 students score second highest
        return 75
    elif average_class_size < 40:
        # Classes with 30 to 39 students score third highest
        return 50
    elif average_class_size < 50:
        # Classes with 40 to 49 students score fourth highest
        return 25
    else:
        # Classes that are 50 or more students receive no credit
        return 0


# Create production functions

def production_average_spending_per_student(dollars, production_efficiency):
    """Production function for the average spending per student attribute"""
    # Educational: spending on instruction, research, and student services
    # Non-educational: spending on sports, dorms, and hospitals
    # Universities will differ in the percentage of dollars spent on educational
    # versus non-educational resources.
    # The educational spending percentage may change from year to year.
    educational_spending_percentage = production_efficiency
    return dollars * educational_spending_percentage


def production_average_class_size(dollars, production_efficiency):
    """Production function for the average class size attribute"""
    class_size_dollars = dollars * production_efficiency
    if class_size_dollars > 10_000:
        return 10
    elif class_size_dollars > 9_000:
        return 20
    elif class_size_dollars > 6_000:
        return 30
    elif class_size_dollars > 3_000:
        return 40
    elif class_size_dollars > 2_000:
        return 50
    elif class_size_dollars > 1_000:
        return 100
    else:
        return 200


# pylint: disable=protected-access
class TestRankingAgent(unittest.TestCase):
    """Unit test class to test the RankingAgent class functions."""

    def setUp(self):
        """Setup the test."""

        # Setup a random seed.
        random_seed = 1234

        # Create a list of M attributes
        # (name, weightage function)
        self.attributes = [Attribute('Average Spending Per Student',
                                     weightage_average_spending_per_student,
                                     valuation_average_spending_per_student,
                                     production_average_spending_per_student),
                           Attribute('Average Class Size',
                                     weightage_average_class_size,
                                     valuation_average_class_size,
                                     production_average_class_size)]

        self.number_of_agents = 2
        self.settings = {'expenditure_min': 5_000, 'expenditure_max': 15_000}

        # Create a new ranking model.
        self.model = RankingModel(self.number_of_agents, self.attributes,
                                  self.settings, random_seed=random_seed)

        # Create a new ranking agent
        self.agent_1 = RankingAgent('Agent_1', self.model)

    def test_optimize_attribute_mix(self):
        """Test the agent optimize attribute mix function."""
        attribute_mix = self.agent_1._optimize_attribute_mix()
        print('attribute_mix = ', attribute_mix)
        self.agent_1.model.schedule.step()
        attribute_mix = self.agent_1._optimize_attribute_mix()
        print('attribute_mix = ', attribute_mix)

    def test_buy_attributes(self):
        """Test the buy attributes function."""

        print("budget = ", self.agent_1._budget)
        self.agent_1.step()
        self.model.schedule.time += 1
        print("funding = ", self.agent_1.attribute_funding)
        print("valuation = ", self.agent_1.attribute_valuation)
        print("weight = ", self.agent_1.attribute_weight)
        print("budget = ", self.agent_1._budget)
        self.agent_1.step()
        self.model.schedule.time += 1
        print("funding = ", self.agent_1.attribute_funding)
        print("valuation = ", self.agent_1.attribute_valuation)
        print("weight = ", self.agent_1.attribute_weight)
        print("budget = ", self.agent_1._budget)
        self.agent_1.step()
        self.model.schedule.time += 1
        print("funding = ", self.agent_1.attribute_funding)
        print("valuation = ", self.agent_1.attribute_valuation)
        print("weight = ", self.agent_1.attribute_weight)

    def test_step(self):
        """Test the step function."""
        self.agent_1.step()
        print(self.agent_1.attribute_funding)
        print(self.agent_1.attribute_valuation)
        print(self.agent_1.attribute_weight)
        print(self.agent_1.score)
        self.agent_1.step()
        print(self.agent_1.attribute_funding)
        print(self.agent_1.attribute_valuation)
        print(self.agent_1.attribute_weight)
        print(self.agent_1.score)


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
