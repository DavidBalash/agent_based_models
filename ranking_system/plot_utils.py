"""Utility functions used to plot."""
import itertools
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display


def get_score_by_agent(model):
    """Get the score by agent dictionary from the model.

    :param model: The ranking model.
    :return: The score by agent dictionary.
    """

    agent_vars_df = model.data_collector.get_agent_vars_dataframe()
    score_by_agent = {}

    for agent, data_frame in agent_vars_df.groupby('AgentID'):
        score_by_agent[agent] = [None]
        for _, row in data_frame.iterrows():
            score_by_agent[agent].append(row.score)

    return score_by_agent


def get_normalized_score_by_agent(model):
    """Get the normalized score by agent dictionary from the model.

    :param model: The ranking model.
    :return: The normalized score by agent dictionary.
    """

    agent_vars_df = model.data_collector.get_agent_vars_dataframe()
    score_by_agent = {}

    for agent, data_frame in agent_vars_df.groupby('AgentID'):
        score_by_agent[agent] = [None]
        for _, row in data_frame.iterrows():
            score_by_agent[agent].append(row.normalized_score)

    return score_by_agent


def display_ranking(model, max_rows=None, all_rows=False):
    """Display the ranking data frame.

    :param model: The model to display.
    :param max_rows: The maximum number of rows to display.
    :param all_rows: All rows boolean flag.
    """
    ranking = model.data_collector.get_table_dataframe('ranking')
    ranking.columns = ['University', 'Time', 'Rank', 'Score',
                       'Normalized Score']
    if all_rows:
        display(ranking)
    elif max_rows is not None:
        with pd.option_context('display.max_rows', max_rows):
            display(ranking)
    else:
        with pd.option_context('display.max_rows', len(model.agents) * 4):
            display(ranking)


# pylint: disable=too-many-arguments
def line_plot(data, xlabel, ylabel, title, xlim_left=None, xlim_right=None,
              ylim_bottom=None, ylim_top=None):
    """Line plot function."""
    if isinstance(data, list):
        list_line_plot(data, xlabel, ylabel, title, xlim_left=xlim_left,
                       xlim_right=xlim_right, ylim_bottom=ylim_bottom,
                       ylim_top=ylim_top)
    elif isinstance(data, dict):
        dictionary_line_plot(data, xlabel, ylabel, title,
                             xlim_left=xlim_left, xlim_right=xlim_right,
                             ylim_bottom=ylim_bottom, ylim_top=ylim_top)


def list_line_plot(data, xlabel, ylabel, title, xlim_left=None, xlim_right=None,
                   ylim_bottom=None, ylim_top=None):
    """Plot the total volatility over time."""

    _, axes = plt.subplots()
    axes.plot(data, marker='s', fillstyle='full', markerfacecolor='w',
              markeredgecolor='grey')
    axes.set(xlabel=xlabel, ylabel=ylabel, title=title)
    plt.xlim(xlim_left, xlim_right)
    plt.ylim(ylim_bottom, ylim_top)
    plt.tick_params(direction='in', top=True, right=True)


def dictionary_line_plot(data, xlabel, ylabel, title, xlim_left=None,
                         xlim_right=None, ylim_bottom=None, ylim_top=None):
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
