"""Run the ranking model."""
import matplotlib.pyplot as plt
import pandas as pd
from commodity import Commodity
from matplotlib.ticker import FuncFormatter
from ranking_model import RankingModel


def _convert_to_ranking_data_frame(input_data_frame):
    data_frame = pd.DataFrame(columns=['period', 'element', 'position'])
    for row in input_data_frame.iterrows():
        for agent in row[1]['Agent rank']:
            position = row[1]['Agent rank']
            ranking = pd.DataFrame([[row[0], agent, position[agent]]],
                                   columns=['period', 'element', 'position'])
            data_frame = data_frame.append(ranking, ignore_index=True)

    data_frame.sort_values(['period', 'element'], inplace=True)
    return data_frame.reset_index(0, drop=True)


number_of_steps = 200
number_of_agents = 5
commodities = [Commodity('commodity-1', 0.6, 0.2),
               Commodity('commodity-2', 0.4, 0.1)]

model = RankingModel(number_of_agents, commodities)
for _ in range(number_of_steps):
    model.step()

model_df = model.data_collector.get_model_vars_dataframe()
ranking_df = _convert_to_ranking_data_frame(model_df)
print(ranking_df.head(10))

agent_df = model.data_collector.get_agent_vars_dataframe()

fig, ax = plt.subplots()

legend_labels = []
for label, df in agent_df.groupby('Unique ID'):
    legend_labels.append(label)
    df.plot(ax=ax)

ax.legend(labels=legend_labels, fontsize="small")
plt.title('Agent score over time')
plt.xlabel('time')
plt.ylabel('score')
plt.xlim(0, number_of_steps)
plt.ylim(0,)

# Don't show the plot grid.
plt.grid(False)

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
