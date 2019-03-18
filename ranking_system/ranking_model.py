"""The ranking model class file."""
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


class RankingModel(Model):
    """The ranking model class."""

    DECIMAL_PLACES = 2

    NORMALIZED_SCORE_RANGE = [0, 100]

    def __init__(self, number_of_agents, attributes, random_seed=None,
                 settings=None):
        """Constructor for the RankingModel class.

        :param number_of_agents: The number of agents.
        :param attributes: The list of attributes.
        :param random_seed: The seed for the random number generator.
        :param settings: The settings dictionary.
        """

        super().__init__()
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

        # Columns used in the ranking table.
        self.rank_columns = ['element', 'period', 'position', 'score',
                             'normalized_score']

        # Columns used in the attribute tables.
        self.attribute_columns = ['element', 'period', 'funding', 'production',
                                  'valuation', 'weight', 'score']

        # Setup tables to add to the data collector
        tables = {'ranking': self.rank_columns}

        # Add a table per attribute
        for index, attribute in enumerate(self.attributes):
            tables[attribute.name] = self.attribute_columns

        # Setup a data collector
        self.data_collector = DataCollector(tables=tables)

        # Remove the position column since it will be added back during the
        # update ranking process
        self.rank_columns.remove('position')

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
        """Update the agent's ranking based on agent score."""
        attribute_scores = []
        for index, _ in enumerate(self.attributes):
            attribute_scores.append([])
        agent_scores = []
        for agent in self.agents:
            agent_scores.append([agent.unique_id, self.schedule.time,
                                 round(agent.score, self.DECIMAL_PLACES),
                                 self._normalize_score(agent.score)])
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

        agent_rank = pd.DataFrame(agent_scores, columns=self.rank_columns)

        # Use pandas data frame to rank the agents.
        agent_rank['position'] =\
            agent_rank['score'].rank(method='min', ascending=False).astype(int)

        for row in agent_rank.to_dict('records'):
            self.data_collector.add_table_row('ranking', row)

        # Add a table per attribute
        for index, attribute in enumerate(self.attributes):
            attribute_score = pd.DataFrame(attribute_scores[index],
                                           columns=self.attribute_columns)
            for row in attribute_score.to_dict('records'):
                self.data_collector.add_table_row(attribute.name, row)

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
