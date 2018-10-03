
from profiling import *


@timed
def generator(n_max):
    return sum(n*n for n in range(1, n_max))


@timed
def for_loop(n_max):
    result = 0
    for n in range(1, n_max):
        result += n*n
    return result


@timed
def list_comprehension(n_max):
    return sum([n*n for n in range(1, n_max)])


# @profiled
# def foo():
#     n_max = 1000
#     return sum(n * n for n in range(1, n_max))


if __name__ == '__main__':
    # print(timeit.timeit('square_sum_comprehension(10)', setup="from __main__ import square_sum_comprehension"))

    with CheckpointTimer("sum of squares", headline=True) as timer:
        generator(10 ** 6)
        timer.checkpoint("generator")

        list_comprehension(10 ** 6)
        timer.checkpoint("comprehension")

        for_loop(10 ** 6)
        timer.checkpoint("for loop")

    print(f"get(...):   {generator.time_taken() * 10**6:.2f} µs")
    print(f"get([...]): {list_comprehension.time_taken() * 10**6:.2f} µs")
    print(f"for ...:    {for_loop.time_taken() * 10**6:.2f} µs")
