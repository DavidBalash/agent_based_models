""" Ranking dynamics and volatility class.

Based on the journal article: Ranking dynamics and volatility [1]

References:
[1] Garcia-Zorita, Carlos & Rousseau, Ronald & Marugan-Lazaro,
Sergio & Casado, Elías. (2018). Ranking dynamics and volatility.
Journal of Informetrics. 12. 567-578. 10.1016/j.joi.2018.04.005.

[2] Marugan-Lazaro, Sergio. (2018). Ranking dynamics and volatility.
GitHub repository, https://github.com/smarugan/uc3m_dynamics

"""
import pandas as pd
from pandas.util.testing import assert_frame_equal
import unittest

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


class RankingDynamicsVolatility:
    """Class used to calculate ranking volatility."""

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
        events_list = []
        for element1 in sorted(self.elements):
            for element2 in sorted(self.elements):
                if element1 == element2:
                    continue
                for period in self.periods:
                    if (period not in self.elements[element1]
                            or period not in self.elements[element2]):
                        continue
                    ranking1 = self.ranking[(self.ranking.element == element1)
                                            & (self.ranking.period == period)]
                    ranking2 = self.ranking[(self.ranking.element == element2)
                                            & (self.ranking.period == period)]
                    events_list.append([ranking2.position.item()
                                       - ranking1.position.item(), 0,
                                       ranking1.element.item(),
                                       ranking2.element.item(),
                                       period, ranking1.position.item(),
                                       ranking2.position.item()])

        events = pd.DataFrame(events_list, columns=['difference',
                                                    'difference_memory',
                                                    'element1', 'element2',
                                                    'period', 'position1',
                                                    'position2'])
        events.sort_values(['element1', 'element2'], inplace=True)

        # Find the tied events in the event data frame..
        tied_events = events[events.difference == 0]

        # For each of the tied events update the difference memory.
        for _, tied in tied_events.iterrows():
            period_index = self.periods.index(tied.period)
            while period_index > 0:
                period_index -= 1
                previous_period = self.periods[period_index]

                # If the elements are not active, break out of the while loop.
                if (previous_period not in self.elements[tied.element1]
                        or previous_period not in self.elements[tied.element2]):
                    break

                # Get the previous row from the event data frame.
                previous = events[(events.element1 == tied.element1)
                                  & (events.element2 == tied.element2)
                                  & (events.period == previous_period)]

                # If the previous difference is not zero then update the
                # difference memory in the event data frame.
                if previous.difference.item() != 0:
                    events.loc[(events.element1 == tied.element1)
                               & (events.element2 == tied.element2)
                               & (events.period == tied.period),
                               'difference_memory'] = previous.difference.item()
                    break

        self._events = events.reset_index(0, drop=True)

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
        if ((event_period_1.difference.item() > 0
             and event_period_2.difference.item() < 0)
                or (event_period_1.difference.item() < 0
                    and event_period_2.difference.item() > 0)):
            return 1

        # If the two elements were tied and are not tied anymore then the last
        # time they were not tied determines if there is a position change.

        # Check ties on period1 -> Use memory
        if ((event_period_1.difference.item() == 0
             and event_period_1.difference_memory.item() > 0
             and event_period_2.difference.item() < 0)
                or (event_period_1.difference.item() == 0
                    and event_period_1.difference_memory.item() < 0
                    and event_period_2.difference.item() > 0)):
            return 1

        # Check ties on period2 -> Use memory
        if ((event_period_2.difference.item() == 0
             and event_period_2.difference_memory.item() > 0
             and event_period_1.difference.item() < 0)
                or (event_period_2.difference.item() == 0
                    and event_period_2.difference_memory.item() < 0
                    and event_period_1.difference.item() > 0)):
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
        volatility = RankingDynamicsVolatility(self.ranking)
        periods = [1, 2, 3, 4]
        self.assertEqual(volatility.periods, periods,
                         'Periods not correct.')
        elements = {'s': [1, 2, 3, 4], 't': [1], 'u': [1, 2, 3, 4], 'v': [1],
                    'w': [2, 3], 'x': [2], 'y': [3, 4], 'z': [4]}
        self.assertEqual(volatility.elements, elements,
                         'Elements not correct')

    def test_create_events(self):
        volatility = RankingDynamicsVolatility(self.ranking)
        volatility._create_events()
        events = pd.read_csv("./unit_test_data/events.csv", index_col=False)
        assert_frame_equal(volatility._events, events)

    def test_calculate_position_shift(self):
        volatility = RankingDynamicsVolatility(self.ranking)
        volatility._create_events()

        # element1 becomes inactive
        shift = volatility._calculate_position_shift('t', 'u', 1, 2)
        self.assertEqual(shift, 1, "Shift result not correct.")

        # element2 becomes inactive
        shift = volatility._calculate_position_shift('s', 't', 1, 2)
        self.assertEqual(shift, 1, "Shift result not correct.")

        # Shift from a negative difference to a positive difference.
        shift = volatility._calculate_position_shift('u', 'y', 3, 4)
        self.assertEqual(shift, 1, "Shift result not correct.")

        # Tied on period1 not tied on period2.
        shift = volatility._calculate_position_shift('s', 'u', 3, 4)
        self.assertEqual(shift, 1, "Shift result not correct.")

        # No shift
        shift = volatility._calculate_position_shift('s', 'u', 2, 3)
        self.assertEqual(shift, 0, "Shift result not correct.")

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
