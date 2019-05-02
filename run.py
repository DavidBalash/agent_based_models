"""Run the ranking model."""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from ranking_system import *

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


# Setup the logger
setup_logging()

# Run settings
RUN_VOLATILITY = False
DISPLAY_LINE_PLOTS = False
DISPLAY_3D_PLOTS = False
DISPLAY_VALUATION_PLOTS = True
DISPLAY_PRODUCTION_PLOTS = False
DISPLAY_SCORE_PLOTS = False

# Model settings
number_of_steps = 10
number_of_agents = 2


# Create weightage functions that will return the weight used for time t
# The sum of the weightage functions at time t must add up to one
def weightage_average_spending_per_student(t):
    """Weight given to average spending per student attribute
       Decreases at time t greater than 5"""
    return 0.7 if t < 5 else 0.6


def weightage_average_class_size(t):
    """Weight given to average class size attribute
       Increases at time t greater than 5"""
    return 0.3 if t < 5 else 0.4


# Create valuation functions
# Return the true valuation of attribute i at time t

def valuation_average_spending_per_student(average_spending_per_student):
    """Valuation given to the average spending per student attribute"""

    # Step like function for average spending per student
    if average_spending_per_student > 10_000:
        # Spending more than 10,000 per student receives the most credit
        return 100
    elif average_spending_per_student > 7_500:
        # Spending between 7,500 and 10,000 per student scores second highest
        return 75
    elif average_spending_per_student > 5_000:
        # Spending between 5,000 and 7,500 per student scores third highest
        return 50
    elif average_spending_per_student > 2_500:
        # Spending between 2,500 and 5,000 per student scores fourth highest
        return 25
    else:
        # Spending less than 2,500 per student receives no credit
        return 0


def valuation_average_class_size(average_class_size):
    """Valuation given to the average class size attribute"""

    # Step like function for average class size
    if average_class_size < 20:
        # Classes with fewer than 20 students receive the most credit
        return 100
    elif average_class_size < 30:
        # Classes with 20 to 29 students score second highest
        return 75
    elif average_class_size < 40:
        # Classes with 30 to 39 students score third highest
        return 50
    elif average_class_size < 50:
        # Classes with 40 to 49 students score fourth highest
        return 25
    else:
        # Classes that are 50 or more students receive no credit
        return 0


# Create production functions

def production_average_spending_per_student(dollars, production_efficiency):
    """Production function for the average spending per student attribute"""
    # Educational: spending on instruction, research, and student services
    # Non-educational: spending on sports, dorms, and hospitals
    # Universities will differ in the percentage of dollars spent on educational
    # versus non-educational resources.
    # The educational spending percentage may change from year to year.
    educational_spending_percentage = production_efficiency
    return dollars * educational_spending_percentage


def production_average_class_size(dollars, production_efficiency):
    """Production function for the average class size attribute"""
    max_value = 15_000
    steepness = 3 * production_efficiency
    return 200 - (200 * np.tanh(np.interp(dollars, [0, max_value],
                                          [0, steepness])))


# Create a list of M attributes
# (name, weightage function)
attributes = [Attribute('Average Spending Per Student',
                        weightage_average_spending_per_student,
                        valuation_average_spending_per_student,
                        production_average_spending_per_student,
                        ),
              Attribute('Average Class Size',
                        weightage_average_class_size,
                        valuation_average_class_size,
                        production_average_class_size)]

settings = {'expenditure_min': 5_000, 'expenditure_max': 15_000}
model = RankingModel(number_of_agents, attributes, settings, random_seed=12345)

if RUN_VOLATILITY:
    normalized_mean_strengths = [None, None]
    volatility_by_agent = {}

    # Setup volatility by agent dictionary
    # by adding an empty list for each agent
    for agent in model.agents:
        volatility_by_agent[agent.unique_id] = [None, None]

    # Manually step though the number of steps
    for step in range(number_of_steps):
        model.step()
        if step > 0:
            model_df = model.data_collector.get_table_dataframe('ranking')
            ranking_dynamics_volatility = RankingDynamicsVolatility(model_df)
            normalized_mean_strengths.append(ranking_dynamics_volatility
                                             .get_normalized_mean_strength())
            total_results = ranking_dynamics_volatility.get_results()
            for _, row in total_results.iterrows():
                volatility_by_agent[row.element].append(row.volatility)

    # Plot the total volatility over time
    line_plot(normalized_mean_strengths, 'time',
              'normalized mean strength (NS)', 'Volatility over time')

    # Plot the agent volatility over time
    line_plot(volatility_by_agent, 'time', 'relative volatility',
              'Agent volatility over time')

    # Plot the agent score over time
    line_plot(find_values_by_agent(model, 'ranking', 'score'), 'time', 'score',
              'Agent score over time')

    plt.show()
else:
    # Run the model for the number of steps
    model.run(number_of_steps)

    display_ranking(model, all_rows=False)

    display_attribute(model, 'Average Spending Per Student', all_rows=False)

    display_attribute(model, 'Average Class Size', all_rows=False)

    display_societal_value(model, all_rows=True)

    display_ranking_dynamics(model, all_rows=True)

    if DISPLAY_PRODUCTION_PLOTS:
        productions = []
        for amount in range(15_000):
            productions.append(production_average_class_size(amount, 0.75))

        _, axes = plt.subplots()
        axes.plot(productions)
        axes.set(xlabel='amount', ylabel='class size',
                 title='Class size by amount')

        productions = []
        for amount in range(15_000):
            productions.append(production_average_spending_per_student(amount,
                                                                       0.75))

        _, axes = plt.subplots()
        axes.plot(productions)
        axes.set(xlabel='amount', ylabel='spending per student',
                 title='Spending per student by amount')

    if DISPLAY_VALUATION_PLOTS:
        amounts = np.linspace(0, 15_000, 1_000_000)
        valuations = []
        for amount in amounts:
            valuations.append(valuation_average_spending_per_student(amount))

        _, axes = plt.subplots()
        axes.plot(amounts, valuations)
        axes.set(xlabel='spending per student', ylabel='score',
                 title='Score by spending per student')

        class_sizes = np.linspace(0, 60, 10_000)
        valuations = []
        for class_size in class_sizes:
            valuations.append(valuation_average_class_size(class_size))

        _, axes = plt.subplots()
        axes.plot(class_sizes, valuations)
        axes.set(xlabel='class size', ylabel='score',
                 title='Score by class size')

    if DISPLAY_SCORE_PLOTS:
        for attribute in model.attributes:
            scores = []
            for amount in range(15_000):
                # Get the weight for this attribute.
                weight = attribute.weightage(1)

                # Get the value of this attribute from the production function.
                efficiency = 0.75
                production = attribute.production(amount, efficiency)

                # Get the valuation of the attribute from valuation function.
                valuation = attribute.valuation(production)

                # Calculate the score of this attribute.
                score = weight * valuation

                scores.append(score)
            _, axes = plt.subplots()
            axes.plot(scores)
            axes.set(xlabel='amount', ylabel='score',
                     title='{} score by spending amount'.format(attribute.name))

    if DISPLAY_3D_PLOTS:
        fig = plt.figure()
        ax = Axes3D(fig)

        xs = []
        ys = []
        zs = []

        for x in range(0, 15_000 + 100, 100):
            for y in range(0, 15_000 + 100, 100):
                xs.append(x)
                ys.append(y)
                zs.append(model.agents[0].objective_function([x, y]))

        ax.plot(xs, ys, zs)

    if DISPLAY_LINE_PLOTS:
        # Plot the normalized score over time
        line_plot(find_values_by_agent(model, 'ranking', 'normalized_score'),
                  'time', 'normalized score', 'Scores over time')

        # Plot the scores over time
        line_plot(find_values_by_agent(model, 'ranking', 'score'), 'time',
                  'score', 'Scores over time')

        # Plot the attribute funding over time
        line_plot(find_values_by_agent(model, 'Average Spending Per Student',
                                       'funding'),
                  'time', 'funding',
                  'Average spending per student funding over time')

        # Plot the societal value over time
        line_plot(table_column_to_list(model, 'societal_value',
                                       'societal_value', [None]),
                  'time', 'societal value', 'Societal value over time')

    # Show the plots
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
