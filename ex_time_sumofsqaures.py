
import functools
import time
# import timeit


def timed(f):
    """
    Decorator that measures the time of execution for a given function
    :param f: Function that is to be timed
    :return: Decorated function
    """
    runs = 10

    @functools.wraps(f)  # Manage introspection, s.a. f.__name__
    def decorated_f(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        for _ in range(2, runs):
            f(*args, **kwargs)
        decorated_f.__time__ = (time.time() - start_time) / runs
        return result

    def get_time():
        return decorated_f.__time__

    decorated_f.__time__ = 0
    decorated_f.time_taken = get_time

    return decorated_f


@timed
def square_sum_generator(n_max):
    return sum(n*n for n in range(1, n_max))


@timed
def square_sum_loop(n_max):
    result = 0
    for n in range(1, n_max):
        result += n*n
    return result


@timed
def square_sum_listcompr(n_max):
    return sum([n*n for n in range(1, n_max)])


if __name__ == '__main__':
    # print(timeit.timeit('square_sum_comprehension(10)', setup="from __main__ import square_sum_comprehension"))

    square_sum_generator(10**6)
    print(f"get(...):   {square_sum_generator.time_taken() * 10**6:.2f} µs")

    square_sum_listcompr(10**6)
    print(f"get([...]): {square_sum_listcompr.time_taken() * 10**6:.2f} µs")

    square_sum_loop(10**6)
    print(f"for ...:    {square_sum_loop.time_taken() * 10**6:.2f} µs")
