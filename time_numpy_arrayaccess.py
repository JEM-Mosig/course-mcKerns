
"""c-Ordered arrays are faster"""


from profiling import CheckpointTimer

if __name__ == '__main__':

    with CheckpointTimer("numpy c-shape", headline=True) as timer:
        import numpy as np
        timer.checkpoint("import numpy")
        x = np.ones((10000000, 2), dtype=np.float32, order='c')
        timer.checkpoint("create array")
        for _ in np.arange(10000000):
            x[0, 0] = x[1, 0]
        timer.checkpoint("x[0, 0] = x[1, 0]")
        for _ in np.arange(10000000):
            x[0, 0] = x[0, 1]
        timer.checkpoint("x[0, 0] = x[0, 1]")

    print()

    with CheckpointTimer("numpy f-shape", headline=True) as timer:
        import numpy as np
        timer.checkpoint("import numpy")
        x = np.ones((10000000, 2), dtype=np.float32, order='f')
        timer.checkpoint("create array")
        for _ in np.arange(10000000):
            x[0, 0] = x[1, 0]
        timer.checkpoint("x[0, 0] = x[1, 0]")
        for _ in np.arange(10000000):
            x[0, 0] = x[0, 1]
        timer.checkpoint("x[0, 0] = x[0, 1]")