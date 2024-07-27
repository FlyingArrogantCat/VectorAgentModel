import numpy as np


class BaseAgent:
    def __init__(self, dim):
        self.dim = dim

        self.state = np.zeros(dim)

    def state_update(self, new_state):

        self.state = new_state


class Agent(BaseAgent):
    def __init__(self, dim_unique, dim_universal):
        self.dim_unique = dim_unique
        self.dim_universal = dim_universal

        self.state_unique = np.zeros(dim_unique)
        self.state_universal = np.zeros(dim_universal)

    def state_update(self, new_state_unique, new_state_universal):

        self.state_unique = new_state_unique
        self.state_universal = new_state_universal
