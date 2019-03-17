"""Utility functions used to plot."""
import itertools
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display


def find_values_by_agent(model, value):
    """Find the values by agent dictionary from the model.

    :param model: The ranking model.
    :param value: The value to find.
    :return: The values by agent dictionary.
    """

    ranking = model.data_collector.get_table_dataframe('ranking')
    normalized_score_by_agent = {}
    for agent, data_frame in ranking.groupby('element'):
        normalized_score_by_agent[agent] = [None]
        for _, row in data_frame.iterrows():
            normalized_score_by_agent[agent].append(row[value])

    return normalized_score_by_agent


def display_ranking(model, max_rows=None, all_rows=False):
    """Display the ranking data frame.

    :param model: The model to display.
    :param max_rows: The maximum number of rows to display.
    :param all_rows: All rows boolean flag.
    """
    ranking = model.data_collector.get_table_dataframe('ranking')
    ranking_columns = ['University', 'Time', 'Rank', 'Score',
                       'Normalized Score']

    # Add attribute related columns
    for i in range(1, len(model.attributes) + 1):
        ranking_columns.append('Funding {}'.format(i))
        ranking_columns.append('Production {}'.format(i))
        ranking_columns.append('Valuation {}'.format(i))
        ranking_columns.append('Weight {}'.format(i))
        ranking_columns.append('Score {}'.format(i))

    ranking.columns = ranking_columns

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
