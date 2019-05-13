"""Unit test for the Ranking Agent class."""
import numpy as np
import unittest
from ranking_system import ClassSizeAttribute
from ranking_system import RankingAgent
from ranking_system import RankingModel
from ranking_system import SpendingPerStudentAttribute
from scipy.optimize import basinhopping

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


def print_fun(x, f, accepted):
    if int(accepted) > 0 and f < 0.0:
        print("x = ", x, "  objective = ", f)


# pylint: disable=protected-access
class TestRankingAgent(unittest.TestCase):
    """Unit test class to test the RankingAgent class functions."""

    def setUp(self):
        """Setup the test."""

        # Setup a random seed.
        random_seed = 1234

        # Create a list of M attributes
        # (name, weightage function)
        self.attributes = [SpendingPerStudentAttribute(), ClassSizeAttribute()]

        self.number_of_agents = 2
        self.settings = {'expenditure_min': 5_000, 'expenditure_max': 15_000}

        # Create a new ranking model.
        self.model = RankingModel(self.number_of_agents, self.attributes,
                                  self.settings, random_seed=random_seed)

        # Create a new ranking agent
        self.agent_1 = RankingAgent('Agent_1', self.model)

    def brute_force_attribute_mix(self):
        best = 0
        best_attribute_mix = [0, 0]
        step = 100

        for amount_1 in range(0, int(self.agent_1._budget) + step, step):
            for amount_2 in range(0, int(self.agent_1._budget) + step, step):
                # Check the budget constraint.
                if amount_1 + amount_2 > int(self.agent_1._budget):
                    continue
                result = self.agent_1.objective_function([amount_1, amount_2])
                if result < best:
                    best = result
                    best_attribute_mix = [amount_1, amount_2]

        print('brute force attribute mix = ', best_attribute_mix)

    def test_optimize_attribute_mix(self):
        """Test the agent optimize attribute mix function."""
        attribute_mix = self.agent_1._optimize_attribute_mix()
        print('attribute_mix = ', attribute_mix)
        self.brute_force_attribute_mix()
        self.agent_1.model.schedule.step()
        attribute_mix = self.agent_1._optimize_attribute_mix()
        print('attribute_mix = ', attribute_mix)
        self.brute_force_attribute_mix()

    def test_optimize_attribute_initial_conditions(self):
        for _ in range(5):
            random_array = np.random.random(len(self.agent_1._inventory))
            x0 = (random_array / random_array.sum()) * self.agent_1._budget
            sol = basinhopping(self.agent_1.objective_function, x0,
                               T=10, stepsize=100,
                               accept_test=self.agent_1._basin_hopping_bounds,
                               # callback=print_fun,
                               minimizer_kwargs={'method': 'BFGS'},
                               niter=2_000)
            print("x0 = ", x0, "  Budget = ", self.agent_1._budget,
                  "  Solution = ", [int(sol.x[0]), int(sol.x[1])],
                  "  objective function result = ",
                  self.agent_1.objective_function([sol.x[0], sol.x[1]]))
        self.agent_1.step()
        random_array = np.random.random(len(self.agent_1._inventory))
        x0 = (random_array / random_array.sum()) * self.agent_1._budget
        sol = basinhopping(self.agent_1.objective_function, x0,
                           T=10, stepsize=100,
                           accept_test=self.agent_1._basin_hopping_bounds,
                           # callback=print_fun,
                           minimizer_kwargs={'method': 'BFGS'},
                           niter=2_000)
        print("x0 = ", x0, "  Budget = ", self.agent_1._budget,
              "  Solution = ", [int(sol.x[0]), int(sol.x[1])],
              "  objective function result = ",
              self.agent_1.objective_function([sol.x[0], sol.x[1]]))

    def test_optimize_attribute_bin_hopping(self):
        random_array = np.random.random(len(self.agent_1._inventory))
        x0 = (random_array / random_array.sum()) * self.agent_1._budget
        print("x0 = ", x0)
        sol = basinhopping(self.agent_1.objective_function, x0,
                           T=10, stepsize=100,
                           accept_test=self.agent_1._basin_hopping_bounds,
                           minimizer_kwargs={'method': 'BFGS'},
                           niter=2_000)
        print("x0 = ", x0, "  Budget = ", self.agent_1._budget,
              "  Solution = ", [int(sol.x[0]), int(sol.x[1])],
              "  objective function result = ",
              self.agent_1.objective_function([sol.x[0], sol.x[1]]))
        self.agent_1.step()
        x0 = [self.agent_1.random.uniform(0, self.agent_1._budget),
              self.agent_1.random.uniform(0, self.agent_1._budget)]
        while sum(x0) > self.agent_1._budget:
            x0 = [self.agent_1.random.uniform(0, self.agent_1._budget),
                  self.agent_1.random.uniform(0, self.agent_1._budget)]
        sol = basinhopping(self.agent_1.objective_function, x0,
                           T=10, stepsize=100,
                           accept_test=self.agent_1._basin_hopping_bounds,
                           minimizer_kwargs={'method': 'BFGS'},
                           niter=2_000)
        print("x0 = ", x0, "  Budget = ", self.agent_1._budget,
              "  Solution = ", [int(sol.x[0]), int(sol.x[1])],
              "  objective function result = ",
              self.agent_1.objective_function([sol.x[0], sol.x[1]]))

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
