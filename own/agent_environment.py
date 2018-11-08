
"""Example of how one might run an agent and an environment in different processes"""

import multiprocessing as mp
import time


class Agent(mp.Process):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.accumulated_reward = 0

    def policy(self, state):
        print(f"{self.name} in state {state} decides to take action {1}")
        return 1

    def run(self):
        # Keep acting until game over
        state, _ = self.environment.recv()
        while state < 10:
            action = self.policy(state)
            self.environment.send(action)

            # While the environment is generating, the agent has time to think
            print(f"{self.name} is thinking...")
            time.sleep(0.1)
            print(f"{self.name} finished thinking.")

            state, reward = self.environment.recv()
            print(f"{self.name} received a reward of {reward}")
            self.accumulated_reward += reward

        print(f"Return = {agent.accumulated_reward}")


class Environment(mp.Process):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.state = 3

    def generate(self, action):
        string = "_" * (self.state - 1) + "A" + "_" * (10 - self.state)

        self.state = self.state + action
        if self.state <= 8:
            reward = 0
        elif self.state == 10:
            reward = 100
        else:
            reward = 1

        string += f" > {reward} > "
        string += "_" * (self.state - 1) + "A" + "_" * (10 - self.state)
        print(string)

        time.sleep(0.05)

        return self.state, reward

    def run(self):
        # Keep generating states as long as agent is alive
        state = self.state
        reward = 0
        while 0 <= state < 10:
            self.agent.send((state, reward))        # Send state and reward to agent
            action = self.agent.recv()              # Receive agent's decision
            state, reward = self.generate(action)   # Generate a new state

        self.agent.send((state, 100))


if __name__ == '__main__':
    a, b = mp.Pipe()

    environment = Environment(a)
    agent = Agent(b)

    environment.start()
    agent.start()

    environment.join()
    agent.join()

