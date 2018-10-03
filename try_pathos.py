
import pathos


def sum_squared(a, b):
    return (a + b)**2


if __name__ == '__main__':
    sp = pathos.pools.SerialPool()
    pp = pathos.pools.ParallelPool()
    mp = pathos.pools.ProcessPool()
    tp = pathos.pools.ThreadPool()

    x = range(5)
    y = range(0, 10, 2)

    for pool in [sp, pp, mp, tp]:
        print(list(pool.map(sum_squared, x, y)))  # List is required for the SerialPool, since it is a generator
        pool.close()  # Close the pool to any new jobs
        pool.join()   # Cleanup the closed worker processes
