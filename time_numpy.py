
"""Importing numpy is slow, and x = x + 1 is faster than x += 1"""


from profiling import CheckpointTimer

if __name__ == '__main__':

    with CheckpointTimer("numpy int", headline=True) as timer:
        import numpy as np
        timer.checkpoint("import numpy")
        x = np.array([1, 2, 3, 4, 5], dtype=np.int)
        y = np.array([1, 2, 3, 4, 5], dtype=np.int)
        timer.checkpoint("create arrays")
        for _ in np.arange(1000000):
            x = x + 1
        timer.checkpoint("x = x + 1")
        for _ in np.arange(1000000):
            y += 1
        timer.checkpoint("y += 1")
        for _ in np.arange(1000000):
            x = x - 1
        timer.checkpoint("x = x - 1")
        for _ in np.arange(1000000):
            y -= 1
        timer.checkpoint("y -= 1")

    print()

    with CheckpointTimer("numpy float32", headline=True) as timer:
        import numpy as np
        timer.checkpoint("import numpy")
        x = np.array([1, 2, 3, 4, 5], dtype=np.float32)
        y = np.array([1, 2, 3, 4, 5], dtype=np.float32)
        timer.checkpoint("create arrays")
        for _ in np.arange(1000000):
            x = x + 1.
        timer.checkpoint("x = x + 1")
        for _ in np.arange(1000000):
            y += 1.
        timer.checkpoint("y += 1")
        for _ in np.arange(1000000):
            x = x - 1.
        timer.checkpoint("x = x - 1")
        for _ in np.arange(1000000):
            y -= 1.
        timer.checkpoint("y -= 1")
