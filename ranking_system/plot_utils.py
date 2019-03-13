"""Utility functions used to plot."""
import itertools
import matplotlib.pyplot as plt


def get_score_by_agent(model):
    """Get the score by agent dictionary from the model.

    :param model: The ranking model.
    :return: The score by agent dictionary.
    """

    agent_vars_df = model.data_collector.get_agent_vars_dataframe()
    score_by_agent = {}

    for agent, data_frame in agent_vars_df.groupby('AgentID'):
        score_by_agent[agent] = []
        for _, row in data_frame.iterrows():
            score_by_agent[agent].append(row.Score)

    return score_by_agent


# pylint: disable=too-many-arguments
def line_plot(data, xlabel, ylabel, title, xlim_left=0, xlim_right=None,
              ylim_bottom=0, ylim_top=None):
    if type(data) is list:
        list_line_plot(data, xlabel, ylabel, title, xlim_left=xlim_left,
                       xlim_right=xlim_right, ylim_bottom=ylim_bottom,
                       ylim_top=ylim_top)
    elif type(data) is dict:
        dictionary_line_plot(data, xlabel, ylabel, title,
                             xlim_left=xlim_left, xlim_right=xlim_right,
                             ylim_bottom=ylim_bottom, ylim_top=ylim_top)


def list_line_plot(data, xlabel, ylabel, title, xlim_left=0, xlim_right=None,
                   ylim_bottom=0, ylim_top=None):
    """Plot the total volatility over time."""

    _, axes = plt.subplots()
    axes.plot(data, marker='s', fillstyle='full', markerfacecolor='w',
              markeredgecolor='grey')
    axes.set(xlabel=xlabel, ylabel=ylabel, title=title)
    plt.xlim(xlim_left, xlim_right)
    plt.ylim(ylim_bottom, ylim_top)
    plt.tick_params(direction='in', top=True, right=True)


def dictionary_line_plot(data, xlabel, ylabel, title, xlim_left=0,
                         xlim_right=None, ylim_bottom=0, ylim_top=None):
    """Plot the agent volatility over time."""

    _, axes = plt.subplots()
    marker = itertools.cycle(('o', 's', 'h', 'd', 'p', 'v', '^', '<', '>', 'H',
                              'D', '*', '|', 'x', '1', '2', '3', '4'))
    legend_labels = []
    for label, y_values in data.items():
        legend_labels.append(label)
        axes.plot(y_values, label=label, marker=next(marker), fillstyle='full',
                  markerfacecolor='w', markeredgecolor='grey')

    axes.set(xlabel=xlabel, ylabel=ylabel, title=title)
    axes.legend(labels=legend_labels, fontsize='small')
    plt.xlim(xlim_left, xlim_right)
    plt.ylim(ylim_bottom, ylim_top)
    plt.tick_params(direction='in', top=True, right=True)
