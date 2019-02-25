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
        self._budget = random.uniform(50, 100)

        # Initialize the random budget increment for this agent.
        self._budget_step_increment_size = random.uniform(50, 100)

        # Initialize the inventory reduction percentage for this agent.
        self._inventory_reduction_percentage = random.uniform(0.5, 0.9)

        # Initialize the agent's inventory.
        self._inventory = []

        # Initialize the agent's score.
        self.score = 0

        # Start with a certain amount of commodities
        self._buy_commodities()
        self._increment_budget()
        self._calculate_score()
        self._utilize_inventory()

    def step(self):
        """The agent's step method.

        This is the agent’s action when it is activated.
        """
        self._buy_commodities()
        self._increment_budget()
        self._calculate_score()
        self._utilize_inventory()

    def _buy_commodities(self):
        """Buy commodities based on price and budget."""
        # Sort the commodities by price descending
        sorted_commodities = sorted(self.model.commodities, reverse=True)

        # Buy as much of the most expensive commodity as possible
        # given the current budget. Followed by buying the next most
        # expensive commodity. Continue until budget does not support
        # further buying.
        for commodity in sorted_commodities:
            if self._budget > commodity.price:
                # Buy the commodity
                quantity, self._budget = divmod(self._budget, commodity.price)

                # Update the inventory
                if commodity in self._inventory:
                    self._inventory.remove(commodity)

                commodity.quantity += quantity
                self._inventory.append(commodity)

    def _utilize_inventory(self):
        """Reduce the current inventory through utilization."""
        # For each item in inventory utilize a random portion.
        for commodity in self._inventory:
            inventory_reduction = round(random.uniform(0.1, 0.2)
                                        * commodity.quantity)
            commodity.quantity -= inventory_reduction

    def _increment_budget(self):
        """Increment the budget based on the income per time step."""
        # Add the income for this step to the budget.
        self._budget += random.uniform(100, 125)

    def _calculate_score(self):
        """Calculate the agent's current score based on inventory."""
        # Reset the score
        self.score = 0

        # For each item in inventory add the quantity times price to the score
        for commodity in self._inventory:
            self.score += commodity.quantity * commodity.price
