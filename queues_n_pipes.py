
"""Demo of multiprocessing queues and pipes"""

import multiprocessing as mp
import pickle


def queue_worker(queue):
    value = queue.get()  # Wait until a value gets sent over the queue `q`
    print(f"Queue worker received '{value}'")


def pipe_worker(pipe):
    message = "Hello, parallel world!"
    print(f"Pipe worker sends '{message}'")
    pipe.send(message)

    value = pipe.recv()  # Receive a value from the pipe

    import pickle
    print(f"Pipe worker received '{value}' and un-pickled it to '{pickle.loads(value)}''")


if __name__ == '__main__':

    print("QUEUE WORKER DEMO")

    q = mp.Queue()
    process = mp.Process(target=queue_worker, args=(q,))
    process.start()

    m = "Message from main process."
    print(f"Main process sends '{m}'")
    q.put(m)
    process.join()

    print()
    print("PIPE WORKER DEMO")

    parent_connection, child_connection = mp.Pipe()
    process = mp.Process(target=pipe_worker, args=(child_connection,))
    process.start()
    m = parent_connection.recv()
    print(f"Main process received '{m}' from pipe worker")

    # noinspection PyRedeclaration
    m = pickle.dumps([1, 2, 3])
    print(f"Main process sends '{m}' to pipe worker")
    parent_connection.send(m)

    process.join()
