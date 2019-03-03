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

    def _calculate_position_shift(self, element1, element2, period1, period2):
        """If there is a position shift between element1 and element2
        in period1 and period2 then return 1 otherwise return 0.

        :param element1: First element to check for a position shift.
        :param element2: Second element to check for a position shift.
        :param period1: First period in which to check for the shift.
        :param period2: Second period in which to check for the shift.
        :return: Return 1 if there is a position shift, else return 0.
        """

        # When the state of one of the two elements changes from active
        # to inactive or from inactive to active return 1.

        # element1 was active and became inactive or
        # element1 was inactive and became active
        if ((period1 in self.elements[element1]
             and period2 not in self.elements[element1])
                or (period1 not in self.elements[element1]
                    and period2 in self.elements[element1])):
            return 1

        # element2 was active and became inactive or
        # element2 was inactive and became active
        if ((period1 in self.elements[element2]
             and period2 not in self.elements[element2])
                or (period1 not in self.elements[element2]
                    and period2 in self.elements[element2])):
            return 1

        # Get the event row from the events data frame that matches the period.
        event_period_1 = self._events[(self._events.element1 == element1)
                                      & (self._events.element2 == element2)
                                      & (self._events.period == period1)]
        event_period_2 = self._events[(self._events.element1 == element1)
                                      & (self._events.element2 == element2)
                                      & (self._events.period == period2)]

        # If both elements do not change state between active or inactive,
        # then we compare the relative position of the element1 and element2
        # between two consecutive periods. If the difference changes to a
        # positive difference or to a negative difference then return 1.
        if ((event_period_1.difference.values[0] > 0
             and event_period_2.difference.values[0] < 0)
                or (event_period_1.difference.values[0] < 0
                    and event_period_2.difference.values[0] > 0)):
            return 1

        # If the two elements were tied and are not tied anymore then the last
        # time they were not tied determines if there is a position change.

        # Check ties on period1 -> Use memory
        if ((event_period_1.difference.values[0] == 0
             and event_period_1.difference_memory.values[0] > 0
             and event_period_2.difference.values[0] < 0)
                or (event_period_1.difference.values[0] == 0
                    and event_period_1.difference_memory.values[0] < 0
                    and event_period_2.difference.values[0] > 0)):
            return 1

        # Check ties on period2 -> Use memory
        if ((event_period_2.difference.values[0] == 0
             and event_period_2.difference_memory.values[0] > 0
             and event_period_1.difference.values[0] < 0)
                or (event_period_2.difference.values[0] == 0
                    and event_period_2.difference_memory.values[0] < 0
                    and event_period_1.difference.values[0] > 0)):
            return 1

        # Otherwise return 0
        return 0


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

    def test_calculate_position_shift(self):
        ranking_dynamics_volatility = RankingDynamicsVolatility(self.ranking)
        ranking_dynamics_volatility._create_events()

        # element1 becomes inactive
        shift = ranking_dynamics_volatility._calculate_position_shift('t', 'u',
                                                                      1, 2)
        self.assertEqual(shift, 1, "Shift result not correct.")

        # element2 becomes inactive
        shift = ranking_dynamics_volatility._calculate_position_shift('s', 't',
                                                                      1, 2)
        self.assertEqual(shift, 1, "Shift result not correct.")

        # Shift from a negative difference to a positive difference.
        shift = ranking_dynamics_volatility._calculate_position_shift('u', 'y',
                                                                      3, 4)
        self.assertEqual(shift, 1, "Shift result not correct.")

        # Tied on period1 not tied on period2.
        shift = ranking_dynamics_volatility._calculate_position_shift('s', 'u',
                                                                      3, 4)
        self.assertEqual(shift, 1, "Shift result not correct.")

        # No shift
        shift = ranking_dynamics_volatility._calculate_position_shift('s', 'u',
                                                                      2, 3)
        self.assertEqual(shift, 0, "Shift result not correct.")
