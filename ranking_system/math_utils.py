"""Math related utility functions."""
import numpy as np


def smooth_step(value, value_range, output_range):
    """The smooth step function provide a smooth transitional step between
       values in a value range.

    :param value: The value to be smoothed.
    :param value_range: The range of input values.
    :param output_range: The range of output values.
    :return: The smooth step value
    """

    interp_range = [-6, 6]
    tanh_range = [-1, 1]
    return np.interp(np.tanh(np.interp(value, value_range, interp_range)),
                     tanh_range, output_range)
