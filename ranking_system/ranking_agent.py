"""Ranking agent class file."""
import copy
import numpy as np
from mesa import Agent
from scipy.optimize import minimize

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
        self._budget = self.random.uniform(model.settings['expenditure_min'],
                                           model.settings['expenditure_max'])

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

        # Start with a certain amount of attributes.
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

        :param variables: The variables used in the objective function.
        :return: The result of applying the objective function to the variables.
        """

        print('variables = ', variables[0], variables[1])
        # sum(weight * valuation(production))
        attribute_scores = []
        for index, attribute in enumerate(self._inventory):
            weight = attribute.weightage(self.model.schedule.time)
            print('weight = ', weight)
            efficiency = self._production_efficiencies[attribute.name]
            print('efficiency = ', efficiency)
            print('variables[index] = ', variables[index])
            production = attribute.production(variables[index], efficiency)
            print('production = ', production)
            valuation = attribute.valuation(production)
            print('valuation = ', valuation)
            score = weight * valuation
            print('score = ', score)
            attribute_scores.append(score)

        # The sign of the return value must be negative because we are going
        # to use the scipy minimize optimization function.
        sign = -1
        print('sum = ', sum(attribute_scores))
        object_function_output = sign * sum(attribute_scores)
        print('objection function output = ', object_function_output)
        return object_function_output

    def _constraint_function(self, variables):
        """The constraint function to be used in the optimization process.

        :param variables: The variables used in the constraint function.
        :return: The constraint function.
        """

        # The constraint function should be negative when the constraint is
        # violated. The sum of the amount allocated to each attribute should
        # be less than the total budget.
        return self._budget - sum(variables)

    def _bounds(self):
        """Get a list of bounds on to be used in the optimization process.

        :return: List of bounds.
        """

        # The bounds on the variables which represent the amount allocated to a
        # particular attribute should be between 0 and the total budget.
        bounds = []
        for _ in self._inventory:
            bounds.append([0, self._budget])
        return bounds

    def _optimize_attribute_mix(self):
        """Optimize the attribute mix."""
        # Minimize a scalar function of one or more variables using
        # Sequential Least SQuares Programming (SLSQP).
        solution = minimize(self._objective_function,
                            np.array([self._budget / 2, self._budget / 2]),
                            method='SLSQP',
                            bounds=self._bounds(),
                            constraints={'type': 'ineq',
                                         'fun': self._constraint_function})
        return solution.x

    def _buy_attributes(self):
        """Buy attributes based on budget."""

        # Use optimization to determine funding allocation.
        funding_allocation = self._optimize_attribute_mix()

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
