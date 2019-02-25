"""The Commodity class represents a commodity in the ranking system."""
from functools import total_ordering


@total_ordering
class Commodity:
    """The Commodity class.

    The Commodity class is comparable and therefore implements
    the __eq__ and __lt__ functions.
    """
    def __init__(self, name, price, depreciation_rate, quantity=0):
        """Initialize the commodity."""
        self.name = name
        self.price = price
        self.depreciation_rate = depreciation_rate
        self.quantity = quantity

    def __eq__(self, other):
        """Check if other commodity price equal.

        :param other: The other commodity to compare.
        :return: True if equal.
        """
        return self.price == other.price

    def __lt__(self, other):
        """Check if the other commodity price is less.

        :param other: The other commodity to compare.
        :return: True if less than.
        """
        return self.price < other.price
