"""Run the ranking model."""
import matplotlib.pyplot as plt
from commodity import Commodity
from matplotlib.ticker import FuncFormatter
from ranking_model import RankingModel

number_of_steps = 200
number_of_agents = 10
commodities = [Commodity('commodity 1', 50, 0.2),
               Commodity('commodity 2', 25, 0.1)]

model = RankingModel(number_of_agents, commodities)
for _ in range(number_of_steps):
    model.step()

agent_df = model.data_collector.get_agent_vars_dataframe()

fig, ax = plt.subplots()

legend_labels = []
for label, df in agent_df.groupby('Unique ID'):
    legend_labels.append(label)
    df.plot(ax=ax)

ax.legend(labels=legend_labels, fontsize="small", bbox_to_anchor=(1, 1),
          loc="upper left")
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
