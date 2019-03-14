"""Unit test for the Ranking Model class."""
import unittest
from ranking_system import RankingModel
from ranking_system import Attribute

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


# pylint: disable=protected-access
class TestRankingModel(unittest.TestCase):
    """Unit test class to test the RankingModel class functions."""

    def setUp(self):
        """Setup the test."""
        seed = 1234
        self.attributes = [Attribute('attribute-1', 0.6),
                           Attribute('attribute-2', 0.4)]
        self.number_of_agents = 5
        self.model = RankingModel(self.number_of_agents, self.attributes,
                                  seed=seed)

    def test_init(self):
        """Test the constructor."""
        self.assertEqual(len(self.model.agents), self.number_of_agents,
                         "Agent size not correct")
        self.assertEqual(len(self.model.attributes), len(self.attributes))

    def test_run(self):
        """Test the run function."""
        number_of_steps = 5
        self.model.run(number_of_steps)
        self.assertEqual(self.model.schedule.steps, number_of_steps)

    def test_step(self):
        """Test the step function."""
        self.model.step()
        self.assertEqual(self.model.schedule.steps, 1)

    def test_current_high_score(self):
        """Test the current high score function."""
        self.model.step()
        self.assertEqual(self.model._current_high_score(), 79.57039673536948)

    def test_normalize_score(self):
        """Test the normalize score function."""
        self.model.step()
        self.assertEqual(self.model._normalize_score(200), 100)


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
