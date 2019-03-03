""" Ranking dynamics and volatility class.

Based on the journal article:
[1] Garcia-Zorita, Carlos & Rousseau, Ronald & Marugan-Lazaro,
Sergio & Casado, Elías. (2018). Ranking dynamics and volatility.
Journal of Informetrics. 12. 567-578. 10.1016/j.joi.2018.04.005.

"""
import pandas as pd
from pandas.util.testing import assert_frame_equal
import unittest


class RankingDynamicsVolatility:
    """Class used calculate ranking volatility."""

    def __init__(self, ranking):
        """The constructor for the RankingDynamicsVolatility class.

        :param ranking: Ranking pandas data frame containing
        the rank for each period for each element being ranked.
        """

        self.ranking = ranking
        self.elements = {}
        self.periods = []

        # For each row in the pandas data frame.
        for _, row in ranking.iterrows():

            if row.element not in self.elements:
                # Add an empty list to the elements dictionary for this element.
                self.elements[row.element] = []

            if row.period not in self.elements[row.element]:
                # Append period to the elements dictionary element period list.
                # This is used for keeping track of period in which the element
                # does not appear in the ranking.
                self.elements[row.element].append(row.period)

            if row.period not in self.periods:
                # Append the period to the period list.
                self.periods.append(row.period)

    def _create_events(self):
        """Create the ranking event data frame."""
        events = []
        for _, row_a in self.ranking.iterrows():
            for _, row_b in self.ranking.iterrows():
                if (row_a.period != row_b.period
                    or (row_a.period == row_b.period
                        and row_a.element == row_b.element)):
                    continue
                events.append([row_b.position - row_a.position, 0,
                               row_a.element, row_b.element,
                               row_a.period, row_a.position,
                               row_b.position])

        event_data_frame = pd.DataFrame(events,
                                        columns=['difference',
                                                 'difference_memory',
                                                 'element1', 'element2',
                                                 'period', 'position1',
                                                 'position2'])
        event_data_frame.sort_values(['element1', 'element2'],
                                     inplace=True)

        # Find the tied events in the event data frame..
        tied_events = event_data_frame[event_data_frame.difference == 0]

        # For each of the tied events update the difference memory.
        for _, tied in tied_events.iterrows():
            period_index = self.periods.index(tied.period)
            while period_index > 0:
                period_index -= 1
                previous_period = self.periods[period_index]

                # If the elements are not active, break out of the while loop.
                if (previous_period not in self.elements[tied.element1] or
                        previous_period not in self.elements[tied.element2]):
                    break

                # Get the previous row from the event data frame.
                previous = event_data_frame[(event_data_frame.element1
                                            == tied.element1) &
                                            (event_data_frame.element2
                                            == tied.element2) &
                                            (event_data_frame.period
                                            == previous_period)]

                # If the previous difference is not zero then update the
                # difference memory in the event data frame, otherwise continue.
                if previous.difference.values[0] != 0:
                    event_data_frame.loc[(event_data_frame.element1
                                         == tied.element1) &
                                         (event_data_frame.element2
                                         == tied.element2) &
                                         (event_data_frame.period
                                         == tied.period),
                                         'difference_memory']\
                        = previous.difference.values[0]
                    break
                else:
                    continue

        self._events = event_data_frame.reset_index(0, drop=True)


class TestRankingDynamicsVolatility(unittest.TestCase):
    """ Unit test class for ranking dynamics volatility functions."""

    def setUp(self):
        # S = {s, t, u, v, w, x, y, z}
        # c1 = (s, t, u, v; [w, x, y, z])
        # c2 = (s, u, w, x; [t, v, y, z])
        # c3 = ([s, u], w, y; [t, v, x, z])
        # c4 = (z, y, u, s; [t, v, w, x])
        # element, period, position
        rank = [['s', 1, 1], ['t', 1, 2], ['u', 1, 3], ['v', 1, 4],
                ['s', 2, 1], ['u', 2, 2], ['w', 2, 3], ['x', 2, 4],
                ['s', 3, 1], ['u', 3, 1], ['w', 3, 3], ['y', 3, 4],
                ['z', 4, 1], ['y', 4, 2], ['u', 4, 3], ['s', 4, 4]]
        self.ranking = pd.DataFrame(rank,
                                    columns=['element', 'period', 'position'])

    def test_init(self):
        ranking_dynamics_volatility = RankingDynamicsVolatility(self.ranking)
        periods = [1, 2, 3, 4]
        self.assertEqual(ranking_dynamics_volatility.periods, periods,
                         'Periods not correct.')
        elements = {'s': [1, 2, 3, 4], 't': [1], 'u': [1, 2, 3, 4], 'v': [1],
                    'w': [2, 3], 'x': [2], 'y': [3, 4], 'z': [4]}
        self.assertEqual(ranking_dynamics_volatility.elements, elements,
                         'Elements not correct')

    def test_create_events(self):
        ranking_dynamics_volatility = RankingDynamicsVolatility(self.ranking)
        ranking_dynamics_volatility._create_events()
        events = pd.read_csv("./unit_test_data/events.csv", index_col=False)
        assert_frame_equal(ranking_dynamics_volatility._events, events)
