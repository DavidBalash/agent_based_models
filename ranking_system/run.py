"""Run the ranking model."""
import plot_utils
import matplotlib.pyplot as plt
from good import Good
from ranking_dynamics_volatility import RankingDynamicsVolatility
from ranking_model import RankingModel

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


number_of_steps = 10
number_of_agents = 5
goods = [Good('good-1', 0.6), Good('good-2', 0.4)]

model = RankingModel(number_of_agents, goods)
normalized_mean_strengths = []
volatility_by_agent = {}

# Setup volatility by agent dictionary by adding an empty list for each agent
for agent in range(number_of_agents):
    volatility_by_agent['agent-{}'.format(agent)] = [None]

# Manually step though the number of steps
for step in range(number_of_steps + 1):
    model.step()
    if step > 0:
        model_df = model.data_collector.get_table_dataframe('Agent rank')
        ranking_dynamics_volatility = RankingDynamicsVolatility(model_df)
        normalized_mean_strengths.append(ranking_dynamics_volatility
                                         .get_normalized_mean_strength())
        total_results = ranking_dynamics_volatility.get_results()
        for _, row in total_results.iterrows():
            volatility_by_agent[row.element].append(row.volatility)
    else:
        normalized_mean_strengths.append(None)


agent_vars_df = model.data_collector.get_agent_vars_dataframe()

score_by_agent = {}
# Setup volatility by agent dictionary by adding an empty list for each agent
for agent, df in agent_vars_df.groupby('Unique ID'):
    score_by_agent[agent] = []
    for _, row in df.iterrows():
        score_by_agent[agent].append(row.Score)

# Plot the total volatility over time
plot_utils.list_line_plot(plt, normalized_mean_strengths, 'time',
                          'normalized mean strength (NS)',
                          'Volatility over time', 1, number_of_steps)


# Plot the agent volatility over time
plot_utils.dictionary_line_plot(plt, volatility_by_agent, 'time',
                                'relative volatility',
                                'Agent volatility over time', 1,
                                number_of_steps)


# Plot the agent score over time
plot_utils.dictionary_line_plot(plt, score_by_agent, 'time',
                                'score',
                                'Agent score over time', 0,
                                number_of_steps)

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
