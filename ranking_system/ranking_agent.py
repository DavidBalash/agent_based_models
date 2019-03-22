"""Ranking agent class file."""
import copy
import logging
from mesa import Agent

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


LOGGER = logging.getLogger('ranking_system.ranking_agent')


class RankingAgent(Agent):
    """The ranking agent class."""

    def __init__(self, unique_id, model):
        """The constructor for the RankingAgent class.

        :param unique_id: the unique identifier for this agent.
        :param model: the model associated with this agent.
        """

        # Call the parent class constructor.
        super().__init__(unique_id, model)
        LOGGER.debug('unique_id = %s', unique_id)

        # Initialize the agent's budget.
        self._budget = self.random.uniform(model.settings['expenditure_min'],
                                           model.settings['expenditure_max'])
        LOGGER.debug('budget = %f', self._budget)

        # Initialize the agent's inventory.
        self._inventory = []

        # Initialize the agent's score.
        self.score = 0

        # Initialize the agent's normalized score.
        self.normalized_score = 0

        # Funding allocated to attributes
        self.attribute_funding = {}

        # Production value of attributes
        self.attribute_production = {}

        # Valuation of attributes
        self.attribute_valuation = {}

        # Weight of attributes
        self.attribute_weight = {}

        # The production efficiencies by attribute
        self._production_efficiencies = {}

        # Setup the attributes.
        for attribute in model.attributes:
            inventory_attribute = copy.deepcopy(attribute)
            self._inventory.append(inventory_attribute)
            self.attribute_funding[attribute.name] = []
            self.attribute_production[attribute.name] = []
            self.attribute_valuation[attribute.name] = []
            self.attribute_weight[attribute.name] = []
            self._production_efficiencies[attribute.name] =\
                model.random.uniform(0.5, 1)

    def step(self):
        """The agent's step method.

        This is the agent’s action when it is activated.
        """

        self._buy_attributes()
        self._increment_budget()
        self._calculate_score()

    def _objective_function(self, variables):
        """The objective function to be used in the optimization process.

        This is the minus one times the sum(weight * valuation(production)) to
        be used in minimization optimization calculation.

        :param variables: The variables used in the objective function.
        :return: The result of applying the objective function to the variables.
        """

        # Calculate the the attribute scores.
        attribute_scores = []
        for index, attribute in enumerate(self._inventory):
            # Get the weight for this attribute.
            weight = attribute.weightage(self.model.schedule.time)

            # Get the true value of this attribute from the production function.
            efficiency = self._production_efficiencies[attribute.name]
            production = attribute.production(variables[index], efficiency)
            LOGGER.debug('funding = %f  efficiency = %f  production = %f',
                         variables[index], efficiency, production)

            # Get the valuation of the attribute from the valuation function.
            valuation = attribute.valuation(production)

            # Calculate the score of this attribute.
            score = weight * valuation
            LOGGER.debug('weight = %f  valuation = %f  score = %f',
                         weight, valuation, score)

            # Append the score to the attribute scores list.
            attribute_scores.append(score)

        # The sign of the return value must be negative because we are going
        # to use the scipy minimize optimization function.
        # sum(weight * valuation(production))
        sum_attribute_scores = sum(attribute_scores)
        LOGGER.debug('sum_attribute_scores = %f', sum_attribute_scores)

        return sum_attribute_scores

    def _optimize_attribute_mix(self):
        """Optimize the attribute mix."""
        best = 0
        best_attribute_mix = [0, 0]
        step_size = 1000

        for amount_1 in range(0, int(self._budget) + step_size, step_size):
            for amount_2 in range(0, int(self._budget) + step_size, step_size):
                # Check the budget constraint.
                if amount_1 + amount_2 > int(self._budget):
                    continue
                result = self._objective_function([amount_1, amount_2])
                if result > best:
                    best = result
                    best_attribute_mix = [amount_1, amount_2]

        return best_attribute_mix

    def _buy_attributes(self):
        """Buy attributes based on budget."""

        # Use optimization to determine funding allocation.
        funding_allocation = self._optimize_attribute_mix()
        LOGGER.debug('funding_allocation = %s', funding_allocation)

        # Randomly allocate funding to attributes.
        for index, attribute in enumerate(self._inventory):
            allocated_funds = funding_allocation[index]
            self.attribute_funding[attribute.name].append(allocated_funds)
            efficiency = self._production_efficiencies[attribute.name]
            attribute.value = attribute.production(allocated_funds, efficiency)
            self.attribute_production[attribute.name].append(attribute.value)
            self._budget -= allocated_funds

    def _increment_budget(self):
        """Increment the budget based on the income per time step."""

        # Add the income for this step to the budget.
        increment = self.random.uniform(self.model.settings['expenditure_min'],
                                        self.model.settings['expenditure_max'])
        self._budget += increment

    def _calculate_score(self):
        """Calculate the agent's current score based on inventory."""

        # Reset the score
        self.score = 0

        # For each attribute in inventory add the attribute value times the
        # attribute weight to the score
        for attribute in self._inventory:
            value = attribute.valuation(attribute.value)
            self.attribute_valuation[attribute.name].append(value)
            weight = attribute.weightage(self.model.schedule.time)
            self.attribute_weight[attribute.name].append(weight)
            self.score += value * weight

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
