"""Ranking agent class file."""
from mesa import Agent
from numpy import random


class RankingAgent(Agent):
    """The ranking agent class."""

    def __init__(self, unique_id, model):
        """The constructor for the RankingAgent class.

        :param unique_id: the unique identifier for this agent.
        :param model: the model associated with this agent.
        """
        super().__init__(unique_id, model)
        # Initialize the agent's budget.
        self._budget = random.uniform(0, 100)

        # Initialize the agent's inventory.
        self._inventory = {}

        # Initialize the agent's score.
        self.score = 0

    def step(self):
        """The agent's step method.

        This is the agent’s action when it is activated.
        """
        self._buy_commodities()
        self._increment_budget()
        self._calculate_score()

    def _buy_commodities(self):
        """Buy commodities based on price and budget."""
        # Sort the commodities by price descending
        sorted_commodities = sorted(self.model.commodity_prices,
                                    key=self.model.commodity_prices.__getitem__,
                                    reverse=True)

        # Buy as much of the most expensive commodity as possible
        # given the current budget. Followed by buying the next most
        # expensive commodity. Continue until budget does not support
        # further buying.
        for index in range(len(sorted_commodities)):
            commodity = sorted_commodities[index]
            price = self.model.commodity_prices[commodity]
            if self._budget > price:
                # Buy the commodity
                quantity, self._budget = divmod(self._budget, price)
                # Update the inventory
                if commodity in self._inventory:
                    self._inventory[commodity] += quantity
                else:
                    self._inventory[commodity] = quantity

    def _increment_budget(self):
        """Increment the budget based on the income per time step."""
        # Add the income for this step to the budget.
        self._budget += random.uniform(0, 50)

    def _calculate_score(self):
        """Calculate the agent's current score based on inventory."""
        # Reset the score
        self.score = 0

        # For each item in inventory add the quantity times price to the score
        for commodity in self._inventory:
            self.score += (self._inventory[commodity]
                           * self.model.commodity_prices[commodity])
