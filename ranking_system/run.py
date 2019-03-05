"""Run the ranking model."""
import matplotlib.pyplot as plt
import pandas as pd
from commodity import Commodity
from matplotlib.ticker import FuncFormatter
from ranking_dynamics_volatility import RankingDynamicsVolatility
from ranking_model import RankingModel

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


def _convert_to_ranking_data_frame(input_data_frame):
    """Convert a ranking model data frame to a ranked data frame."""
    data_frame = pd.DataFrame(columns=['element', 'period', 'position'])
    for row in input_data_frame.iterrows():
        for agent in row[1]['Agent rank']:
            position = row[1]['Agent rank']
            ranking = pd.DataFrame([[agent, row[0], position[agent]]],
                                   columns=['element', 'period', 'position'])
            data_frame = data_frame.append(ranking, ignore_index=True)

    data_frame.sort_values(['period', 'element'], inplace=True)
    return data_frame.reset_index(0, drop=True)


number_of_steps = 10
number_of_agents = 8
commodities = [Commodity('commodity-1', 0.6, 0.2),
               Commodity('commodity-2', 0.4, 0.1)]


model = RankingModel(number_of_agents, commodities)
normalized_mean_strengths = []
for step in range(number_of_steps + 1):
    model.step()
    if step > 0:
        model_df = model.data_collector.get_table_dataframe('Agent rank')
        ranking_dynamics_volatility = RankingDynamicsVolatility(model_df)
        normalized_mean_strengths.append(ranking_dynamics_volatility
                                         .get_normalized_mean_strength())
    else:
        normalized_mean_strengths.append(None)

# results = ranking_dynamics_volatility.get_results()
# results.to_csv('results.csv', index=False, header=True)
# ranking_df = _convert_to_ranking_data_frame(model_df)
# ranking_df.to_csv("./rank.csv", sep=";", index=False, header=True)

# event_df = _create_ranking_event_data_frame(ranking_df)
# event_df.to_csv("./event.csv", sep=",", index=False, header=True)

fig1, ax1 = plt.subplots()
ax1.plot(normalized_mean_strengths)
ax1.plot(normalized_mean_strengths, 's', fillstyle='full', color='w',
         markeredgecolor='grey')
ax1.set(xlabel='time', ylabel='normalized mean strength (NS)',
        title='Volatility')
ax1.grid(False)  # (axis='y', linestyle='--')
plt.xlim(1, number_of_steps)
# plt.ylim(0, 1)
# Set the plot tick parameters so that the ticks are facing inward and on both
# the top and the bottom of the plot.
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
