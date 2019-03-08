"""Run the ranking model."""
import matplotlib.pyplot as plt
from commodity import Commodity
from matplotlib.ticker import FuncFormatter
from ranking_dynamics_volatility import RankingDynamicsVolatility
from ranking_model import RankingModel

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


number_of_steps = 10
number_of_agents = 8
commodities = [Commodity('commodity-1', 0.6, 0.2),
               Commodity('commodity-2', 0.4, 0.1)]


model = RankingModel(number_of_agents, commodities)
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


fig1, ax1 = plt.subplots()
ax1.plot(normalized_mean_strengths)
ax1.plot(normalized_mean_strengths, 's', fillstyle='full', color='w',
         markeredgecolor='grey')
ax1.set(xlabel='time', ylabel='normalized mean strength (NS)',
        title='Volatility over time')
ax1.grid(False)  # (axis='y', linestyle='--')
plt.xlim(1, number_of_steps)
plt.ylim(0,)
# Set the plot tick parameters so that the ticks are facing inward and on both
# the top and the bottom of the plot.
plt.tick_params(direction='in', top=True, right=True)

legend_labels = []
fig2, ax2 = plt.subplots()
for agent, volatility in volatility_by_agent.items():
    legend_labels.append(agent)
    ax2.plot(volatility, label=agent)

ax2.set(xlabel='time', ylabel='relative volatility',
        title='Agent volatility over time')
ax2.legend(labels=legend_labels, fontsize='small')
plt.xlim(1, number_of_steps)
plt.ylim(0,)
plt.tick_params(direction='in', top=True, right=True)

agent_df = model.data_collector.get_agent_vars_dataframe()

fig, ax = plt.subplots()

legend_labels = []
for label, df in agent_df.groupby('Unique ID'):
    legend_labels.append(label)
    df.plot(ax=ax)

ax.legend(labels=legend_labels, fontsize='small')
ax.set(xlabel='time', ylabel='score', title='Agent score over time')
ax.grid(False)

plt.xlim(0, number_of_steps)
plt.ylim(0,)

# Set the plot tick parameters so that the ticks are facing inward and on both
# the top and the bottom of the plot.
plt.tick_params(direction='in', top=True, right=True)


def format_fn(tick_val, _):
    """Tick formatting function.
    :param tick_val: The tick value used to determine label.
    :param _: An unused parameter tick_pos.
    :return: The label for the tick value.
    """
    if int(tick_val) in range(1, number_of_steps):
        return int(tick_val)
    else:
        return ''


ax.xaxis.set_major_formatter(FuncFormatter(format_fn))

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
