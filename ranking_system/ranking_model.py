"""The ranking model class file."""
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from ranking_agent import RankingAgent


class RankingModel(Model):
    """The ranking model class."""

    def __init__(self, number_of_agents, commodities):
        """Constructor for the RankingModel class.

        :param commodities: The list of commodities.
        """
        super().__init__()
        self._agents = []
        self.agent_rank = {}
        self.commodities = commodities

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
            model_reporters={"Agent rank": "agent_rank"},
            # An agent attribute
            agent_reporters={"Score": "score", "Unique ID": "unique_id"})

    def step(self):
        """Advance the model by one step."""
        self.data_collector.collect(self)

        # When we call the schedule’s step method, it shuffles the order of the
        # agents, then activates them all, one at a time.
        self.schedule.step()

        # Update the agent ranking
        self._update_ranking()

    def _update_ranking(self):
        """Update the agent's ranking based on agent score."""
        agent_scores = {}
        for agent in self._agents:
            agent_scores[agent.unique_id] = agent.score

        self.agent_rank = {key: rank for rank, key in
                           enumerate(sorted(agent_scores, key=agent_scores.get,
                                            reverse=True), 1)}
