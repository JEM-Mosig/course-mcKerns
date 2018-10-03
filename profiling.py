
import functools
import time
# import timeit
import cProfile


def timed(f):
    """
    Decorator that measures the time of execution for a given function

    The time is stored as introspection parameter that can be accessed
    with f.time_taken().
    :param f: Function that is to be timed
    :return: Decorated function
    """
    runs = 10

    @functools.wraps(f)  # Manage introspection, s.a. f.__name__
    def decorated_f(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)  # Run once to get the result
        for _ in range(2, runs):     # Run a few more times to improve timing statistic
            f(*args, **kwargs)
        decorated_f.__time__ = (time.time() - start_time) / runs
        return result

    def get_time():
        return decorated_f.__time__

    decorated_f.__time__ = 0
    decorated_f.time_taken = get_time

    return decorated_f


class CheckpointTimer:
    """
    Timer that can be used to profile multiple lines of code

    For example
        with CheckpointTimer("expensive stuff") as timer:
          expensive_foo()
          timer.checkpoint("expensive_foo")
          expensive_bar()
          timer.checkpoint("expensive_bar")
    reports the total and lapse times of expensive_foo and expensive_bar.
    Based on https://zapier.com/engineering/profiling-python-boss/
    """
    def __init__(self, name="", silent=False, headline=False):
        self._name = name
        self._silent = silent      # False: only print times, True: only memorize times
        self._log = []             # List of checkpoint outputs

        if headline:
            message = " ".ljust(len(name)) + " |    TOTAL    |    LAPSE    |"
            if self._silent:
                self._log.append(message)
            else:
                print(message)

        self._start = time.time()  # Time of creation
        self._lap = self._start    # Time of last checkpoint

    @property
    def elapsed(self):
        now = time.time()
        return now - self._start, now - self._lap

    @staticmethod
    def _auto_unit(value):
        if value < 10**-6:
            return 10**9 * value, "ns"
        elif value < 10**-3:
            return 10**6 * value, "µs"
        elif value < 1.0:
            return 10**3 * value, "ms"
        elif value < 10**3:
            return value, " s"
        elif value < 10**6:
            return 10**-3 * value, "ks"

    def checkpoint(self, name=''):
        total, laps = self.elapsed
        total, total_unit = self._auto_unit(total)
        laps, laps_unit = self._auto_unit(laps)
        message = f"{self._name} | {total: >8.4f} {total_unit} | {laps: >8.4f} {laps_unit} | {name}"
        if self._silent:
            self._log.append(message)
        else:
            print(message)
        self._lap = time.time()

    def print_log(self):
        for entry in self._log:
            print(entry)
        pass

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.checkpoint("FINISHED")
        pass


def profiled(f):
    """
    Decorator that profiles the given function and returns the original function
    :param f: Function that is to be profiled
    :return: f
    """
    print("PROFILING: " + f.__name__ + "()")
    cProfile.runctx(f.__name__ + "()", globals(), locals())  # ToDo: Allow parameters

    return f
