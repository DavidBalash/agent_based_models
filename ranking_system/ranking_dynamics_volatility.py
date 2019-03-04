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
        self._total_results, self._normalized_mean_strength =\
            self._calculate_volatility()

    def _create_events(self):
        """Create the ranking event data frame.
        :return: event data frame
        """

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

        # For each of the tied events update the difference memory.
        for _, tied in events[events.difference == 0].iterrows():
            tied_index = self._periods.index(tied.period)
            for period_index in reversed(range(1, tied_index)):
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

    # Disabling chained comparison pylint warning because the chained
    # comparisons make more sense when reading the following code.
    # pylint: disable=chained-comparison
    def _calculate_position_shift(self, element1, element2, period1, period2):
        """If there is a position shift between element1 and element2
        in period1 and period2 then return 1 otherwise return 0.

        :param element1: First element to check for a position shift.
        :param element2: Second element to check for a position shift.
        :param period1: First period in which to check for the shift.
        :param period2: Second period in which to check for the shift.
        :return: Return 1 if there is a position shift, else return 0.
        """

        # If there is a positional shift set this boolean variable to true.
        is_position_shift = False

        # When the state of one of the two elements changes from active
        # to inactive or from inactive to active return 1.

        # element1 was active and became inactive
        if (period1 in self._elements[element1]
                and period2 not in self._elements[element1]):
            is_position_shift = True

        # element1 was inactive and became active
        elif (period1 not in self._elements[element1]
              and period2 in self._elements[element1]):
            is_position_shift = True

        # element2 was active and became inactive
        elif (period1 in self._elements[element2]
              and period2 not in self._elements[element2]):
            is_position_shift = True

        # element2 was inactive and became active
        elif (period1 not in self._elements[element2]
              and period2 in self._elements[element2]):
            is_position_shift = True

        else:
            # Get the event period rows from the events data frame that match
            # the elements and the period.
            event_period_1 = self._events[(self._events.element1 == element1)
                                          & (self._events.element2 == element2)
                                          & (self._events.period == period1)]
            event_period_2 = self._events[(self._events.element1 == element1)
                                          & (self._events.element2 == element2)
                                          & (self._events.period == period2)]

            # If the event period rows are both not empty check the event
            # periods for shifts.
            if not event_period_1.empty and not event_period_2.empty:
                # If both elements do not change state between active or
                # inactive, then we compare the relative position of the
                # element1 and element2 between two consecutive periods.
                # If the difference changes to a positive difference or to a
                # negative difference then return 1.
                if (event_period_1.difference.item() > 0
                        and event_period_2.difference.item() < 0):
                    is_position_shift = True

                elif (event_period_1.difference.item() < 0
                      and event_period_2.difference.item() > 0):
                    is_position_shift = True

                # If the two elements were tied and the two elements are not
                # tied anymore then the last time they were not tied determines
                # if there is a change.

                # Check ties on period1 -> Use memory
                elif (event_period_1.difference.item() == 0
                      and event_period_1.difference_memory.item() > 0
                      and event_period_2.difference.item() < 0):
                    is_position_shift = True

                elif (event_period_1.difference.item() == 0
                      and event_period_1.difference_memory.item() < 0
                      and event_period_2.difference.item() > 0):
                    is_position_shift = True

                # Check ties on period2 -> Use memory
                elif (event_period_2.difference.item() == 0
                      and event_period_2.difference_memory.item() > 0
                      and event_period_1.difference.item() < 0):
                    is_position_shift = True

                elif (event_period_2.difference.item() == 0
                      and event_period_2.difference_memory.item() < 0
                      and event_period_1.difference.item() > 0):
                    is_position_shift = True

        return 1 if is_position_shift else 0

    def _calculate_volatility(self):
        """Calculate the partial and total volatility.
        :return: A tuple of total results and normalized mean strength.
        """

        # Calculate the maximum number of shifts.
        max_shifts = (len(self._elements) - 1) * (len(self._periods) - 1)

        # Partial Result: element1, element2, position_shifts
        partial_result = {'element1': [], 'element2': [], 'position_shifts': []}

        # Total Result: element, max_shifts, position_shifts, volatility
        total_result = {'element': [], 'max_shifts': [],
                        'position_shifts': [], 'volatility': []}

        # Store the total volatility.
        total_volatility = 0

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
            total_volatility += position_shifts

        self._partial_results = pd.DataFrame(partial_result)

        # Normalized mean strength is the total volatility divided by the number
        # of element to element comparisons between each period. The number of
        # comparisons is the number of elements, times the number of elements
        # minus one, times the number of periods minus one.
        normalized_mean_strength = (total_volatility
                                    / (len(self._elements)
                                       * (len(self._elements) - 1)
                                       * (len(self._periods) - 1)))

        return pd.DataFrame(total_result), normalized_mean_strength

    def get_results(self):
        """Get the total results in a pandas data frame.
        :return: A pandas data frame containing the total results.
        """

        return self._total_results

    def get_normalized_mean_strength(self):
        """Get the normalized mean strength.
        :return: normalized mean strength
        """

        return self._normalized_mean_strength


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
