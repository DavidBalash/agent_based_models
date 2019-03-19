"""Run the ranking model."""
import matplotlib.pyplot as plt
from ranking_system import *

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"

RUN_VOLATILITY = False

number_of_steps = 10
number_of_agents = 5


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


def production_average_spending_per_student(dollars, random):
    """Production function for the average spending per student attribute"""
    # Educational: spending on instruction, research, and student services
    # Non-educational: spending on sports, dorms, and hospitals
    # Universities will differ in the percentage of dollars spent on educational
    # versus non-educational resources.
    # The educational spending percentage may change from year to year.
    educational_spending_percentage = random.uniform(0.5, 1)
    return dollars * educational_spending_percentage


def production_average_class_size(dollars, random):
    """Production function for the average class size attribute"""
    if dollars > random.uniform(9_000, 10_000):
        return 10
    elif dollars > random.uniform(6_000, 9_000):
        return 20
    elif dollars > random.uniform(3_000, 6_000):
        return 30
    elif dollars > random.uniform(2_000, 3_000):
        return 40
    elif dollars > random.uniform(1_000, 2_000):
        return 50
    elif dollars > random.uniform(500, 1_000):
        return 100
    else:
        return 200


# Create a list of M attributes
# (name, weightage function)
attributes = [Attribute('Average Spending Per Student',
                        weightage_average_spending_per_student,
                        valuation_average_spending_per_student,
                        production_average_spending_per_student),
              Attribute('Average Class Size',
                        weightage_average_class_size,
                        valuation_average_class_size,
                        production_average_class_size)]

settings = {'expenditure_min': 5_000, 'expenditure_max': 15_000}
model = RankingModel(number_of_agents, attributes, settings)

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
    # Manually step though the number of steps
    for step in range(number_of_steps):
        model.step()

    display_ranking(model, all_rows=False)

    display_attribute(model, 'Average Spending Per Student', all_rows=False)

    display_attribute(model, 'Average Class Size', all_rows=False)

    line_plot(find_values_by_agent(model, 'ranking', 'normalized_score'),
              'time', 'normalized score', 'Scores over time')

    line_plot(find_values_by_agent(model, 'ranking', 'score'), 'time', 'score',
              'Scores over time')

    # Plot the attribute funding over time
    line_plot(find_values_by_agent(model, 'Average Spending Per Student',
                                   'funding'),
              'time', 'funding',
              'Average spending per student funding over time')

    display_societal_value(model, all_rows=True)

    line_plot(table_column_to_list(model, 'societal_value', 'societal_value',
                                   [None]), 'time', 'societal value',
              'Societal value over time')

    display_ranking_dynamics(model, all_rows=True)

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
