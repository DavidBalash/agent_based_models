""" Unit test for Ranking dynamics and volatility class."""
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from ranking_dynamics_volatility import RankingDynamicsVolatility

__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"


# pylint: disable=protected-access
class TestRankingDynamicsVolatility(unittest.TestCase):
    """ Unit test class for ranking dynamics volatility functions."""

    def setUp(self):
        """Unit test setup method."""

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
        """Test the init for the RankingDynamicsVolatility class."""

        volatility = RankingDynamicsVolatility(self._ranking)
        periods = [1, 2, 3, 4]
        self.assertEqual(volatility._periods, periods,
                         'Periods not correct.')
        elements = {'s': [1, 2, 3, 4], 't': [1], 'u': [1, 2, 3, 4], 'v': [1],
                    'w': [2, 3], 'x': [2], 'y': [3, 4], 'z': [4]}
        self.assertEqual(volatility._elements, elements,
                         'Elements not correct')

    def test_create_events(self):
        """Test the create events function."""

        volatility = RankingDynamicsVolatility(self._ranking)
        events = pd.read_csv('./unit_test_data/events.csv', index_col=False)
        assert_frame_equal(volatility._events, events)

    def test_calculate_position_shift(self):
        """Test the calculate position shift function."""

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
        """Test the calculate volatility function."""

        volatility = RankingDynamicsVolatility(self._ranking)
        total_results = volatility.get_results()
        partial_results = pd.read_csv('./unit_test_data/partial_results.csv',
                                      index_col=False)
        results = pd.read_csv('./unit_test_data/results.csv', index_col=False)
        assert_frame_equal(volatility._partial_results, partial_results)
        assert_frame_equal(total_results, results)
        total_volatility = 0
        for _, row in total_results.iterrows():
            total_volatility += row.position_shifts
        number_of_comparisons = (len(volatility._elements)
                                 * (len(volatility._elements) - 1)
                                 * (len(volatility._periods) - 1))
        normalized_mean_strength = total_volatility / number_of_comparisons
        self.assertEqual(number_of_comparisons, 168,
                         'Number of comparisons not correct.')
        self.assertEqual(total_volatility, 102,
                         'Total volatility not correct.')
        self.assertEqual(volatility.get_normalized_mean_strength(),
                         normalized_mean_strength,
                         'Normalized mean strength not correct.')

    def test_get_results(self):
        """Test the volatility results."""

        ranking = pd.read_csv('./unit_test_data/ranking.csv', index_col=False)
        volatility = RankingDynamicsVolatility(ranking)
        results = volatility.get_results()
        total_results = pd.read_csv('./unit_test_data/total_results.csv',
                                    index_col=False)
        assert_frame_equal(results, total_results)
        self.assertEqual(results.size, total_results.size,
                         'Result size not correct.')


if __name__ == '__main__':
    unittest.main()

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
