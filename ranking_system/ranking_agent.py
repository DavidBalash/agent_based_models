"""Ranking agent class file."""
import copy
from mesa import Agent

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


class RankingAgent(Agent):
    """The ranking agent class."""

    def __init__(self, unique_id, model):
        """The constructor for the RankingAgent class.

        :param unique_id: the unique identifier for this agent.
        :param model: the model associated with this agent.
        """

        super().__init__(unique_id, model)
        # Initialize the agent's production input elasticity value alpha.
        self._alpha = self.random.random()

        # Initialize the agent's budget.
        self._budget = self.random.uniform(50, 100)

        # Initialize the random budget increment for this agent.
        self._budget_step_increment_size = self.random.uniform(50, 100)

        # Initialize the agent's inventory.
        self._inventory = []

        # Initialize the agent's score.
        self.score = 0

        # Initialize the agent's normalized score.
        self.normalized_score = 0

        # Start with a certain amount of attributes.
        for attribute in self.model.attributes:
            inventory_attribute = copy.deepcopy(attribute)
            inventory_attribute.set_quantity(self.random.uniform(50, 75))
            self._inventory.append(inventory_attribute)

    def step(self):
        """The agent's step method.

        This is the agent’s action when it is activated.
        """

        self._buy_attributes()
        self._increment_budget()
        self._calculate_score()

    def _buy_attributes(self):
        """Buy attributes based on budget."""

        # Randomly buy attributes.
        for attribute in self._inventory:
            capital_expenditure = self.random.uniform(0, self._budget)
            attribute.simple_production_function(capital_expenditure,
                                                 self.random.random())
            self._budget -= capital_expenditure

    def _increment_budget(self):
        """Increment the budget based on the income per time step."""

        # Add the income for this step to the budget.
        self._budget += self._budget_step_increment_size

    def _calculate_score(self):
        """Calculate the agent's current score based on inventory."""

        # Reset the score
        self.score = 0

        # For each item in inventory add the ranking value the score
        for attribute in self._inventory:
            self.score += attribute.valuation(self.model.schedule.time)

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
