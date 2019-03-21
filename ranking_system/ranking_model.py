"""The ranking model class file."""
import itertools
import logging.config
import numpy as np
import pandas as pd
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from .ranking_agent import RankingAgent

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


LOGGER = logging.getLogger('ranking_system.ranking_model')


class RankingModel(Model):
    """The ranking model class."""

    DECIMAL_PLACES = 2

    NORMALIZED_SCORE_RANGE = [0, 100]

    def __init__(self, number_of_agents, attributes, settings=None,
                 random_seed=None):
        """Constructor for the RankingModel class.

        :param number_of_agents: The number of agents.
        :param attributes: The list of attributes.
        :param settings: The settings dictionary.
        :param random_seed: The seed for the random number generator.
        """

        super().__init__()
        LOGGER.debug('number_of_agents = %f', number_of_agents)
        LOGGER.debug('attributes = %s', attributes)
        LOGGER.debug('settings = %s', settings)
        LOGGER.debug('random_seed = %s', random_seed)

        self.reset_randomizer(random_seed)
        self.agents = []
        self.attributes = attributes
        self.settings = settings if settings is not None else {}

        # The RandomActivation scheduler activates all the agents once per
        # step, in random order.
        self.schedule = RandomActivation(self)

        # Create and schedule ranking agents.
        for agent_count in range(1, number_of_agents + 1):
            unique_id = "University {}".format(agent_count)
            agent = RankingAgent(unique_id, self)
            self.agents.append(agent)
            self.schedule.add(agent)

        # Setup tables to add to the data collector
        tables = {'ranking': ['element', 'period', 'position', 'score',
                              'normalized_score'],
                  'societal_value': ['period', 'societal_value'],
                  'ranking_dynamics': ['period', 'distance', 'society_delta',
                                       'gamma']}

        # Add a table per attribute
        for attribute in self.attributes:
            tables[attribute.name] = ['element', 'period', 'funding',
                                      'production', 'valuation', 'weight',
                                      'score']

        # Setup a data collector
        self.data_collector = DataCollector(tables=tables)

    def run(self, number_of_steps):
        """Run the model for the input number of time steps.

        :param number_of_steps: The number of time steps to run the model.
        """

        for _ in range(number_of_steps):
            self.step()

    def step(self):
        """Advance the model by one step."""

        # When we call the schedule’s step method, it shuffles the order of the
        # agents, then activates them all, one at a time.
        self.schedule.step()

        # Update the agent ranking
        self._update_ranking()

        # Update the agent attribute scores
        self._update_attribute_scores()

        # Update the societal value table
        self._update_societal_value()

        # Update the ranking dynamics table
        self._update_ranking_dynamics()

        # Collect data.
        self.data_collector.collect(self)

    def _current_high_score(self):
        """Get the current high score.

        :return: The high score value.
        """

        scores = []
        for agent in self.agents:
            scores.append(agent.score)

        return max(scores)

    def _normalize_score(self, score):
        """Normalize the score.

        :param score: The score to normalize.
        :return: The normalized score.
        """

        score_interval = [0, self._current_high_score()]
        return int(round(np.interp(score, score_interval,
                                   self.NORMALIZED_SCORE_RANGE)))

    def _update_ranking(self):
        """Update each agent's ranking based on agent score."""

        # Get the current agent scores.
        agent_scores = []
        for agent in self.agents:
            agent_scores.append([agent.unique_id, self.schedule.time,
                                 round(agent.score, self.DECIMAL_PLACES),
                                 self._normalize_score(agent.score)])

        # Get the ranking columns from the ranking table.
        ranking_columns = list(self.data_collector.
                               get_table_dataframe('ranking'))

        # Remove the position column since it will be added back after ranking.
        ranking_columns.remove('position')
        agent_rank = pd.DataFrame(agent_scores, columns=ranking_columns)

        # Use pandas data frame to rank the agents.
        agent_rank['position'] =\
            agent_rank['score'].rank(method='min', ascending=False).astype(int)

        # Add the records as a row in the ranking table.
        for row in agent_rank.to_dict('records'):
            self.data_collector.add_table_row('ranking', row)

    def _update_attribute_scores(self):
        """Update each agent's attribute scores and related values."""

        # Initialize the attribute scores list.
        attribute_scores = list(itertools.repeat([], len(self.attributes)))

        # For each agent and each attribute append to the attribute scores list.
        for agent in self.agents:
            for index, attribute in enumerate(self.attributes):
                step_index = self.schedule.time - 1
                funds = agent.attribute_funding[attribute.name][step_index]
                produce = agent.attribute_production[attribute.name][step_index]
                value = agent.attribute_valuation[attribute.name][step_index]
                weight = agent.attribute_weight[attribute.name][step_index]
                attributes = [agent.unique_id, self.schedule.time,
                              round(funds, self.DECIMAL_PLACES),
                              round(produce, self.DECIMAL_PLACES),
                              round(value, self.DECIMAL_PLACES),
                              round(weight, self.DECIMAL_PLACES),
                              round(value * weight, self.DECIMAL_PLACES)]
                attribute_scores[index].append(attributes)

        # Add a table per attribute
        for index, attribute in enumerate(self.attributes):
            attribute_columns = list(self.data_collector.
                                     get_table_dataframe(attribute.name))
            attribute_score = pd.DataFrame(attribute_scores[index],
                                           columns=attribute_columns)
            # Add the attribute scores as a row in the attribute score table.
            for row in attribute_score.to_dict('records'):
                self.data_collector.add_table_row(attribute.name, row)

    def _update_ranking_dynamics(self):
        """Update the ranking dynamics table."""

        # If we are not the the second scheduled time step yet then return.
        if self.schedule.time < 2:
            return

        distance = 0

        ranking = self.data_collector.get_table_dataframe('ranking')
        for agent, data_frame in ranking.groupby('element'):
            delta = 0
            for _, row in data_frame.iterrows():
                if row['period'] == self.schedule.time - 1:
                    delta = row['position']
                elif row['period'] == self.schedule.time:
                    delta -= row['position']
            if delta > 0:
                distance += delta
            LOGGER.debug("agent = %s  distance = %f", agent, distance)

        society = self.data_collector.get_table_dataframe('societal_value')
        society_t = 0
        society_t_minus_one = 0
        for _, row in society.iterrows():
            if row['period'] == self.schedule.time - 1:
                society_t_minus_one = row['societal_value']
            elif row['period'] == self.schedule.time:
                society_t = row['societal_value']

        society_delta = society_t - society_t_minus_one

        # Calculate gamma
        gamma = 0
        if society_delta > 0:
            gamma = distance / society_delta

        # Build the ranking dynamics row.
        ranking_dynamics_row = {'period': self.schedule.time,
                                'distance': distance,
                                'society_delta': round(society_delta,
                                                       self.DECIMAL_PLACES),
                                'gamma': gamma}

        # Add the ranking dynamics row to the ranking dynamics table.
        self.data_collector.add_table_row('ranking_dynamics',
                                          ranking_dynamics_row)

    def _update_societal_value(self):
        """Update the societal value table."""

        # Sum the production values over all agents and all of their attributes.
        sum_production_values = 0
        for agent in self.agents:
            for attribute in self.attributes:
                step_index = self.schedule.time - 1
                produce = agent.attribute_production[attribute.name][step_index]
                sum_production_values += produce

        # Build the societal value row.
        societal_value_row = {'period': self.schedule.time,
                              'societal_value': round(sum_production_values,
                                                      self.DECIMAL_PLACES)}

        # Add the societal value row to the societal value table.
        self.data_collector.add_table_row('societal_value', societal_value_row)


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
