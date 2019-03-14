"""The ranking model class file."""
import numpy as np
import pandas as pd
from IPython.display import display
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

    def __init__(self, number_of_agents, attributes, settings=None):
        """Constructor for the RankingModel class.

        :param number_of_agents: The number of agents.
        :param attributes: The list of attributes.
        :param settings: The settings dictionary.
        """

        super().__init__()
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

        # Setup a data collector
        self.data_collector = DataCollector(
            # A model attribute
            tables={"ranking": ["element", "period", "position", "score",
                                "normalized_score"]},
            # An agent attribute
            agent_reporters={"score": "score",
                             "normalized_score": "normalized_score"})

        # Collect data at time t = 0
        # self._update_ranking()
        # self.data_collector.collect(self)

    def display_ranking(self, max_rows=None, all_rows=False):
        ranking = self.data_collector.get_table_dataframe('ranking')
        ranking.columns = ['University', 'Time', 'Rank', 'Score',
                           'Normalized Score']
        if all_rows:
            display(ranking)
        elif max_rows is not None:
            with pd.option_context('display.max_rows', max_rows):
                display(ranking)
        else:
            with pd.option_context('display.max_rows', len(self.agents) * 4):
                display(ranking)

    def run(self, number_of_steps):
        """Run the model for the input number of time steps.

        :param number_of_steps: The number of time steps to run the model.
        """

        for step in range(number_of_steps):
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

        agent_scores = []
        for agent in self.agents:
            agent.normalized_score = self._normalize_score(agent.score)
            agent_scores.append([agent.unique_id,
                                 self.schedule.time,
                                 round(agent.score, self.DECIMAL_PLACES),
                                 agent.normalized_score])

        agent_rank = pd.DataFrame(agent_scores,
                                  columns=['element', 'period', 'score',
                                           'normalized_score'])

        # Use pandas data frame to rank the agents.
        agent_rank['position'] =\
            agent_rank['normalized_score'].rank(method='min',
                                                ascending=False).astype(int)

        for row in agent_rank.to_dict('records'):
            self.data_collector.add_table_row("ranking", row)

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
