"""Utility functions used to plot."""
import itertools
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display


def find_values_by_agent(model, table_name, value):
    """Find the values by agent dictionary from the model.

    :param model: The ranking model.
    :param table_name: The table used to find the values.
    :param value: The value to find.
    :return: The values by agent dictionary.
    """

    ranking = model.data_collector.get_table_dataframe(table_name)
    value_by_agent = {}
    for agent, data_frame in ranking.groupby('element'):
        value_by_agent[agent] = [None]
        for _, row in data_frame.iterrows():
            value_by_agent[agent].append(row[value])

    return value_by_agent


def table_column_to_list(model, table_name, column_name, start_at_one=True):
    """Get a column from a table as a list.

    :param model: The model where the table resides.
    :param table_name: The name of the table.
    :param column_name: The name of the column to convert to a list.
    :param start_at_one: If true start the list from index 1.
    :return: Table column as a list.
    """

    table = model.data_collector.get_table_dataframe(table_name)
    column_as_list = table[column_name].tolist()
    return [None] + column_as_list if start_at_one else column_as_list


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


def display_attribute(model, attribute_name, max_rows=None, all_rows=False):
    """Display the attribute data frame.

    :param model: The model with attributes to display.
    :param attribute_name: The name of the attribute to display.
    :param max_rows: The maximum number of rows to display.
    :param all_rows: All rows boolean flag.
    """
    attributes = model.data_collector.get_table_dataframe(attribute_name)
    attributes.columns = ['University', 'Time', 'Funding', 'Production',
                          'Valuation', 'Weight', 'Score']
    if all_rows:
        display(attributes)
    elif max_rows is not None:
        with pd.option_context('display.max_rows', max_rows):
            display(attributes)
    else:
        with pd.option_context('display.max_rows', len(model.agents) * 4):
            display(attributes)


def display_societal_value(model, max_rows=None, all_rows=False):
    """Display the societal value data frame.

    :param model: The model with attributes to display.
    :param max_rows: The maximum number of rows to display.
    :param all_rows: All rows boolean flag.
    """
    societal_values = model.data_collector.get_table_dataframe('societal_value')
    societal_values.columns = ['Time', 'Societal Value']

    societal_values.loc['Total', 'Time'] = ''

    societal_values.loc['Total', 'Societal Value'] =\
        round(societal_values['Societal Value'].sum(), model.DECIMAL_PLACES)

    if all_rows:
        display(societal_values)
    elif max_rows is not None:
        with pd.option_context('display.max_rows', max_rows):
            display(societal_values)
    else:
        with pd.option_context('display.max_rows', len(model.agents) * 4):
            display(societal_values)


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
