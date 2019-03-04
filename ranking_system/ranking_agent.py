"""Ranking agent class file."""
from mesa import Agent
from numpy import random
import copy

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
        # Initialize the agent's budget.
        self._budget = random.uniform(50, 100)

        # Initialize the random budget increment for this agent.
        self._budget_step_increment_size = random.uniform(50, 100)

        # Initialize the agent's inventory.
        self._inventory = []

        # Initialize the agent's score.
        self.score = 0

        # Start with a certain amount of commodities
        for commodity in self.model.commodities:
            inventory_commodity = copy.deepcopy(commodity)
            inventory_commodity.quantity = random.uniform(150, 200)
            self._inventory.append(inventory_commodity)

        # Calculate the initial score
        self._calculate_score()

    def step(self):
        """The agent's step method.

        This is the agent’s action when it is activated.
        """
        self._buy_commodities()
        self._increment_budget()
        self._calculate_score()
        self._depreciate_inventory()

    def _buy_commodities(self):
        """Buy commodities based on budget."""
        # Randomly buy commodities.
        for commodity in self._inventory:
            purchase_amount = random.uniform(0, self._budget)
            commodity.quantity += purchase_amount
            self._budget -= purchase_amount

    def _depreciate_inventory(self):
        """Reduce the current inventory through utilization."""
        # For each item in inventory utilize a random portion.
        for commodity in self._inventory:
            commodity.depreciate()

    def _increment_budget(self):
        """Increment the budget based on the income per time step."""
        # Add the income for this step to the budget.
        self._budget += self._budget_step_increment_size

    def _calculate_score(self):
        """Calculate the agent's current score based on inventory."""
        # Reset the score
        self.score = 0

        # For each item in inventory add the quantity times price to the score
        for commodity in self._inventory:
            self.score += commodity.total_value()

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
