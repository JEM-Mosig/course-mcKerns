
"""Demo of shared c-types with numpy"""

import multiprocessing as mp

from multiprocessing import sharedctypes
from numpy import ctypeslib


def fill_array(arr, value):
    arr.fill(value)


if __name__ == '__main__':

    # Create an array of integers on c-level
    raw_array = sharedctypes.RawArray('i', 4)

    # Convert the raw array into a numpy c-object
    array = ctypeslib.as_array(raw_array)

    # Reshape in-place
    array.shape = (2, 2)

    # Create two processes which write on different rows of `array`
    process1 = mp.Process(target=fill_array, args=(array[0, :], 5))
    process2 = mp.Process(target=fill_array, args=(array[1, :], 7))

    # Start both processes and wait for them to finish
    process1.start()
    process2.start()
    process1.join()
    process2.join()

    print(array)  # [[5 5] \ [7 7]]
