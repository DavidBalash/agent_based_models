"""The ranking model class file."""
import pandas as pd
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from .ranking_agent import RankingAgent

__name__ = "ranking_model"
__package__ = "ranking_system"
__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


class RankingModel(Model):
    """The ranking model class."""

    def __init__(self, number_of_agents, attributes):
        """Constructor for the RankingModel class.

        :param number_of_agents: The number of agents.
        :param attributes: The list of attributes.
        """

        super().__init__()
        self._agents = []
        self.attributes = attributes

        # The RandomActivation scheduler activates all the agents once per
        # step, in random order.
        self.schedule = RandomActivation(self)

        # Create and schedule ranking agents.
        for agent_count in range(number_of_agents):
            unique_id = "agent-{}".format(agent_count)
            agent = RankingAgent(unique_id, self)
            self._agents.append(agent)
            self.schedule.add(agent)

        # Setup a data collector
        self.data_collector = DataCollector(
            # A model attribute
            tables={"Agent rank": ["element", "period", "position", "score"]},
            # An agent attribute
            agent_reporters={"Score": "score", "Unique ID": "unique_id"})

        # Collect data at time t = 0
        self.data_collector.collect(self)

    def step(self):
        """Advance the model by one step."""

        # When we call the schedule’s step method, it shuffles the order of the
        # agents, then activates them all, one at a time.
        self.schedule.step()

        # Update the agent ranking
        self._update_ranking()

        # Collect data.
        self.data_collector.collect(self)

    def _update_ranking(self):
        """Update the agent's ranking based on agent score."""

        agent_scores = []
        for agent in self._agents:
            agent_scores.append([agent.unique_id,
                                 self.schedule.time,
                                 agent.score])

        agent_rank = pd.DataFrame(agent_scores,
                                  columns=['element', 'period', 'score'])

        # Use pandas data frame to rank the agents.
        agent_rank['position'] = agent_rank['score'].rank(ascending=False)

        for row in agent_rank.to_dict('records'):
            self.data_collector.add_table_row("Agent rank", row)

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
