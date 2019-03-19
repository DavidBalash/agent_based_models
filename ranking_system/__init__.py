"""Ranking system package."""
from .attribute import Attribute
from .plot_utils import dictionary_line_plot
from .plot_utils import display_attribute
from .plot_utils import display_ranking_dynamics
from .plot_utils import display_ranking
from .plot_utils import display_societal_value
from .plot_utils import find_values_by_agent
from .plot_utils import line_plot
from .plot_utils import list_line_plot
from .plot_utils import table_column_to_list
from .ranking_agent import RankingAgent
from .ranking_dynamics_volatility import RankingDynamicsVolatility
from .ranking_model import RankingModel

__all__ = ["Attribute", "dictionary_line_plot", "display_attribute",
           "display_ranking", "display_ranking_dynamics",
           "display_societal_value", "find_values_by_agent", "line_plot",
           "list_line_plot", "table_column_to_list", "RankingAgent",
           "RankingDynamicsVolatility", "RankingModel"]

__title__ = "ranking_system"
__author__ = "David Balash"
__copyright__ = "Copyright 2019, Agent Based Models"
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Prototype"

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
