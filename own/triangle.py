
import multiprocessing as mp


def worker_a(pipe_control, pipe_b, pipe_c):
    pipe_control.recv()  # Wait until controller has created all the workers and pipes

    message = "XXX"
    print(f"A sends '{message}' to B")
    pipe_b.send(message)

    value = pipe_c.recv()  # Receive a value from pipe_c
    print(f"A received '{value}' from C")


def worker_b(pipe_a, pipe_c):
    value = pipe_a.recv()
    print(f"B received '{value}' from A")

    message = f"Passing on {value}"
    print(f"B sends '{message}' to C")
    pipe_c.send(message)


def worker_c(pipe_a, pipe_b):
    value = pipe_b.recv()
    print(f"C received '{value}' from B")

    message = f"Passing on {value}"
    print(f"C sends '{message}' to A")
    pipe_a.send(message)


if __name__ == '__main__':
    parent_connection_ab, child_connection_ab = mp.Pipe()
    parent_connection_bc, child_connection_bc = mp.Pipe()
    parent_connection_ca, child_connection_ca = mp.Pipe()
    parent_connection, child_connection = mp.Pipe()

    process_a = mp.Process(target=worker_a, args=(child_connection, parent_connection_ab, child_connection_ca))
    process_b = mp.Process(target=worker_b, args=(child_connection_ab, parent_connection_bc))
    process_c = mp.Process(target=worker_c, args=(parent_connection_ca, child_connection_bc))

    process_c.start()
    process_a.start()
    process_b.start()

    print("Go!")
    parent_connection.send(1)
    process_a.join()
    process_b.join()
    process_c.join()
    print("Done.")
