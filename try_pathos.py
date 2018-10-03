
import pathos
from profiling import CheckpointTimer


def sum_squared(a, b):
    return (a + b)**2


if __name__ == '__main__':
    sp = pathos.pools.SerialPool()
    pp = pathos.pools.ParallelPool()
    mp = pathos.pools.ProcessPool()
    tp = pathos.pools.ThreadPool()

    x = range(500)
    y = range(0, 1000, 2)

    with CheckpointTimer("pathos") as timer:
        list(sp.map(sum_squared, x, y))  # List is required for the SerialPool, since it is a generator
        sp.close()  # Close the pool to any new jobs
        sp.join()   # Cleanup the closed worker processes
        timer.checkpoint("Serial")

        pp.map(sum_squared, x, y)
        pp.close()  # Close the pool to any new jobs
        pp.join()   # Cleanup the closed worker processes
        timer.checkpoint("Parallel")

        mp.map(sum_squared, x, y)
        mp.close()  # Close the pool to any new jobs
        mp.join()   # Cleanup the closed worker processes
        timer.checkpoint("Process")

        tp.map(sum_squared, x, y)
        tp.close()  # Close the pool to any new jobs
        tp.join()   # Cleanup the closed worker processes
        timer.checkpoint("Thread")
