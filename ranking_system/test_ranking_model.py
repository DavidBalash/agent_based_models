"""Unit test for the Ranking Model class."""
import unittest
from ranking_system import Attribute
from ranking_system import RankingModel

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


def weightage_function_1(time_step):
    """Weightage function."""
    return [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3][time_step]


def weightage_function_2(time_step):
    """Weightage function."""
    return [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7][time_step]


def valuation_function_1(value):
    """Valuation function."""
    return value


def valuation_function_2(value):
    """Valuation function."""
    return value


def production_function_1(dollars, production_efficiency):
    """Production function."""
    return dollars * production_efficiency


def production_function_2(dollars, production_efficiency):
    """Production function."""
    return dollars * production_efficiency


# pylint: disable=protected-access
class TestRankingModel(unittest.TestCase):
    """Unit test class to test the RankingModel class functions."""

    def setUp(self):
        """Setup the test."""

        # Setup a random seed.
        random_seed = 1234

        # Create attributes.
        self.attribute_1 = Attribute('attribute_1', weightage_function_1,
                                     valuation_function_1,
                                     production_function_1)
        self.attribute_2 = Attribute('attribute_2', weightage_function_2,
                                     valuation_function_2,
                                     production_function_2)

        self.attributes = [self.attribute_1, self.attribute_2]
        self.number_of_agents = 2
        self.settings = {'expenditure_min': 5_000, 'expenditure_max': 15_000}

        # Create a new ranking model.
        self.model = RankingModel(self.number_of_agents, self.attributes,
                                  self.settings, random_seed=random_seed)

    def test_init(self):
        """Test the constructor."""

        self.assertEqual(len(self.model.agents), self.number_of_agents,
                         "Agent size not correct.")
        self.assertEqual(len(self.model.attributes), len(self.attributes),
                         "Attributes size not correct.")

    def test_run(self):
        """Test the run function."""

        number_of_steps = 5
        self.model.run(number_of_steps)
        self.assertEqual(self.model.schedule.steps, number_of_steps,
                         'Number of model steps not equal.')

    def test_step(self):
        """Test the step function."""

        self.model.step()
        self.assertEqual(self.model.schedule.steps, 1, 'Model steps not equal.')

    def test_current_high_score(self):
        """Test the current high score function."""

        self.model.step()
        self.assertGreater(self.model._current_high_score(), 0,
                           'Current high score less than 0.')

    def test_normalize_score(self):
        """Test the normalize score function."""

        self.model.step()
        self.assertGreaterEqual(self.model._normalize_score(200), 0,
                                'Normalized score less than 0.')
        self.assertLessEqual(self.model._normalize_score(200), 100,
                             'Normalized score greater than 100.')


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
