# Inspired by https://pymotw.com/2/multiprocessing/communication.html

"""Use a queue to distribute tasks over many agents, and another queue to collect all results"""


import multiprocessing as mp
import time


class Worker(mp.Process):
    def __init__(self, queue_in, queue_out):
        super().__init__()
        self.queue_in = queue_in
        self.queue_out = queue_out

    def work(self, task):
        time.sleep(0.1)
        return f"{task} was completed by {self.name}"

    def run(self):
        # Keep working until 'None' task is given
        task = self.queue_in.get()
        while task is not None:
            print(f"{self.name} works on {task}")
            product = self.work(task)       # Work on the task
            self.queue_out.put(product)     # Return result
            self.queue_in.task_done()       # Notify in-queue that this task is done
            task = self.queue_in.get()      # Ask for a new task

        print(f"Worker {self.name} is done with all tasks.")
        self.queue_in.task_done()


if __name__ == '__main__':

    NUM_WORKERS = 9
    NUM_TASKS = 20

    tasks = mp.JoinableQueue()
    results = mp.Queue()

    workers = [Worker(tasks, results) for i in range(NUM_WORKERS)]

    for worker in workers:
        worker.start()

    for i in range(NUM_TASKS):
        tasks.put(f"Task {i+1}")

    for i in range(NUM_WORKERS):
        tasks.put(None)

    tasks.join()

    for i in range(NUM_TASKS):
        print(results.get())