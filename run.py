"""Run the ranking model."""
import matplotlib.pyplot as plt
from ranking_system import *

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"

RUN_VOLATILITY = False

number_of_steps = 10
number_of_agents = 5


# Create weightage functions that will return the weight used for time t
# The sum of the weightage functions at time t must add up to one
def weightage_1(t):
    """Weight given to attribute l changes at time t greater than 5"""
    return 0.7 if t < 5 else 0.6


def weightage_2(t):
    """Weight given to attribute 2 changes at time t greater than 5"""
    return 0.3 if t < 5 else 0.4


# Create a list of M attributes
# (name, weightage function)
attributes = [Attribute('research', weightage_1),
              Attribute('faculty', weightage_2)]

model = RankingModel(number_of_agents, attributes)

if RUN_VOLATILITY:
    normalized_mean_strengths = [None, None]
    volatility_by_agent = {}

    # Setup volatility by agent dictionary
    # by adding an empty list for each agent
    for agent in model.agents:
        volatility_by_agent[agent.unique_id] = [None, None]

    # Manually step though the number of steps
    for step in range(number_of_steps):
        model.step()
        if step > 0:
            model_df = model.data_collector.get_table_dataframe('ranking')
            ranking_dynamics_volatility = RankingDynamicsVolatility(model_df)
            normalized_mean_strengths.append(ranking_dynamics_volatility
                                             .get_normalized_mean_strength())
            total_results = ranking_dynamics_volatility.get_results()
            for _, row in total_results.iterrows():
                volatility_by_agent[row.element].append(row.volatility)

    # Plot the total volatility over time
    line_plot(normalized_mean_strengths, 'time',
              'normalized mean strength (NS)', 'Volatility over time')

    # Plot the agent volatility over time
    line_plot(volatility_by_agent, 'time', 'relative volatility',
              'Agent volatility over time')

    # Plot the agent score over time
    line_plot(get_score_by_agent(model), 'time', 'score',
              'Agent score over time')

    plt.show()
else:
    # Manually step though the number of steps
    for step in range(number_of_steps):
        model.step()

    display_ranking(model, all_rows=False)

    line_plot(get_normalized_score_by_agent(model), 'time', 'normalized score',
              'Scores over time')

    line_plot(get_score_by_agent(model), 'time', 'score', 'Scores over time')

    plt.show()

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
