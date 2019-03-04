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

        self._ranking = ranking
        self._elements = {}
        self._periods = []

        # For each row in the pandas data frame.
        for _, row in ranking.iterrows():

            if row.element not in self._elements:
                # Add an empty list to the elements dictionary for this element.
                self._elements[row.element] = []

            if row.period not in self._elements[row.element]:
                # Append period to the elements dictionary element period list.
                # This is used for keeping track of period in which the element
                # does not appear in the ranking.
                self._elements[row.element].append(row.period)

            if row.period not in self._periods:
                # Append the period to the period list.
                self._periods.append(row.period)

        # Create the events used to calculate the volatility.
        self._events = self._create_events()

        # Calculate the total volatility results.
        self._total_results = self._calculate_volatility()

    def _create_events(self):
        """Create the ranking event data frame."""
        events_list = []
        for element1 in sorted(self._elements):
            for element2 in sorted(self._elements):
                if element1 == element2:
                    continue
                for period in self._periods:
                    if (period not in self._elements[element1]
                            or period not in self._elements[element2]):
                        continue
                    ranking1 = self._ranking[(self._ranking.element == element1)
                                             & (self._ranking.period == period)]
                    ranking2 = self._ranking[(self._ranking.element == element2)
                                             & (self._ranking.period == period)]
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

        # Find the tied events in the event data frame.
        tied_events = events[events.difference == 0]

        # For each of the tied events update the difference memory.
        for _, tied in tied_events.iterrows():
            period_index = self._periods.index(tied.period)
            while period_index > 0:
                period_index -= 1
                prev_period = self._periods[period_index]

                # If the elements are not active, break out of the while loop.
                if (prev_period not in self._elements[tied.element1]
                        or prev_period not in self._elements[tied.element2]):
                    break

                # Get the previous row from the event data frame.
                previous = events[(events.element1 == tied.element1)
                                  & (events.element2 == tied.element2)
                                  & (events.period == prev_period)]

                # If the previous difference is not zero then update the
                # difference memory in the event data frame.
                if previous.difference.item() != 0:
                    events.loc[(events.element1 == tied.element1)
                               & (events.element2 == tied.element2)
                               & (events.period == tied.period),
                               'difference_memory'] = previous.difference.item()
                    break

        return events.reset_index(0, drop=True)

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
        if ((period1 in self._elements[element1]
             and period2 not in self._elements[element1])
                or (period1 not in self._elements[element1]
                    and period2 in self._elements[element1])):
            return 1

        # element2 was active and became inactive or
        # element2 was inactive and became active
        if ((period1 in self._elements[element2]
             and period2 not in self._elements[element2])
                or (period1 not in self._elements[element2]
                    and period2 in self._elements[element2])):
            return 1

        # Get the event row from the events data frame that matches the period.
        event_period_1 = self._events[(self._events.element1 == element1)
                                      & (self._events.element2 == element2)
                                      & (self._events.period == period1)]
        event_period_2 = self._events[(self._events.element1 == element1)
                                      & (self._events.element2 == element2)
                                      & (self._events.period == period2)]

        # If the event rows are empty return 0.
        if event_period_1.empty or event_period_2.empty:
            return 0

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

    def _calculate_volatility(self):
        """Calculate the partial and total volatility."""

        # Calculate the maximum number of shifts.
        max_shifts = (len(self._elements) - 1) * (len(self._periods) - 1)

        # Partial Result: element1, element2, position_shifts
        partial_result = {'element1': [], 'element2': [], 'position_shifts': []}

        # Total Result: element, max_shifts, position_shifts, volatility
        total_result = {'element': [], 'max_shifts': [],
                        'position_shifts': [], 'volatility': []}

        for result_index, element1 in enumerate(sorted(self._elements)):
            total_result['element'].append(element1)
            total_result['position_shifts'].append(0)
            for element2 in sorted(self._elements):
                if element1 == element2:
                    continue

                total_shifts = 0
                for period, next_period in zip(self._periods[:-1],
                                               self._periods[1:]):
                    event_shift = self._calculate_position_shift(element1,
                                                                 element2,
                                                                 period,
                                                                 next_period)
                    total_shifts += event_shift

                partial_result['element1'].append(element1)
                partial_result['element2'].append(element2)
                partial_result['position_shifts'].append(total_shifts)

                total_result['position_shifts'][result_index] += total_shifts

            total_result['max_shifts'].append(max_shifts)
            position_shifts = total_result['position_shifts'][result_index]
            total_result['volatility'].append(position_shifts / max_shifts)

        self._partial_results = pd.DataFrame(partial_result)

        return pd.DataFrame(total_result)

    def get_results(self):
        return self._total_results


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
        self._ranking = pd.DataFrame(rank,
                                     columns=['element', 'period', 'position'])

    def test_init(self):
        volatility = RankingDynamicsVolatility(self._ranking)
        periods = [1, 2, 3, 4]
        self.assertEqual(volatility._periods, periods,
                         'Periods not correct.')
        elements = {'s': [1, 2, 3, 4], 't': [1], 'u': [1, 2, 3, 4], 'v': [1],
                    'w': [2, 3], 'x': [2], 'y': [3, 4], 'z': [4]}
        self.assertEqual(volatility._elements, elements,
                         'Elements not correct')

    def test_create_events(self):
        volatility = RankingDynamicsVolatility(self._ranking)
        events = pd.read_csv('./unit_test_data/events.csv', index_col=False)
        assert_frame_equal(volatility._events, events)

    def test_calculate_position_shift(self):
        volatility = RankingDynamicsVolatility(self._ranking)

        # element1 becomes inactive
        position_shift = volatility._calculate_position_shift('t', 'u', 1, 2)
        self.assertEqual(position_shift, 1,
                         'Position shift result not correct.')

        # element2 becomes inactive
        position_shift = volatility._calculate_position_shift('s', 't', 1, 2)
        self.assertEqual(position_shift, 1,
                         'Position shift result not correct.')

        # Shift from a negative difference to a positive difference.
        position_shift = volatility._calculate_position_shift('u', 'y', 3, 4)
        self.assertEqual(position_shift, 1,
                         'Position shift result not correct.')

        # Tied on period1 not tied on period2.
        position_shift = volatility._calculate_position_shift('s', 'u', 3, 4)
        self.assertEqual(position_shift, 1,
                         'Position shift result not correct.')

        # No position shift
        position_shift = volatility._calculate_position_shift('s', 'u', 2, 3)
        self.assertEqual(position_shift, 0,
                         'Position shift result not correct.')

    def test_calculate_volatility(self):
        volatility = RankingDynamicsVolatility(self._ranking)
        results = pd.read_csv('./unit_test_data/results.csv', index_col=False)
        total_results = volatility.get_results()
        print(total_results)
        assert_frame_equal(total_results, results)

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
