"""Run the ranking model."""
import matplotlib.pyplot as plt
from ranking_system import *

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


number_of_steps = 10
number_of_agents = 5
attributes = [Attribute('attribute-1', 0.6), Attribute('attribute-2', 0.4)]

model = RankingModel(number_of_agents, attributes)
normalized_mean_strengths = []
volatility_by_agent = {}

# Setup volatility by agent dictionary by adding an empty list for each agent
for agent in model.agents:
    volatility_by_agent[agent.unique_id] = [None]

# Manually step though the number of steps
for step in range(number_of_steps + 1):
    model.step()
    if step > 0:
        model_df = model.data_collector.get_table_dataframe('ranking')
        ranking_dynamics_volatility = RankingDynamicsVolatility(model_df)
        normalized_mean_strengths.append(ranking_dynamics_volatility
                                         .get_normalized_mean_strength())
        total_results = ranking_dynamics_volatility.get_results()
        for _, row in total_results.iterrows():
            volatility_by_agent[row.element].append(row.volatility)
    else:
        normalized_mean_strengths.append(None)


# Plot the total volatility over time
line_plot(normalized_mean_strengths, 'time', 'normalized mean strength (NS)',
          'Volatility over time')

# Plot the agent volatility over time
line_plot(volatility_by_agent, 'time', 'relative volatility',
          'Agent volatility over time')

# Plot the agent score over time
line_plot(get_score_by_agent(model), 'time', 'score', 'Agent score over time')

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
