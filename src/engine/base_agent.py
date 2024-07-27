import numpy as np


class BaseAgent:
    def __init__(self, dim, state=None):
        self.dim = dim

        self.state = np.zeros(dim) if state is None else state

    def state_update(self, new_state):

        self.state = new_state


class Agent(BaseAgent):
    def __init__(self, dim:int, dim_unique:int, dim_universal:int):
        super(Agent, self).__init__(dim=dim)
        assert dim > dim_unique + dim_universal, f"Incorrect input {dim}"

        self.dim_unique = dim_unique
        self.dim_universal = dim_universal

        self.actualized_universal_dims = np.arange(0, dim_universal)
        self.actualized_unique_dims = np.arange(dim_universal, dim_universal + dim_unique)

        self.culture_indx = 0

    def state_update(self, new_state_unique, new_state_universal):

        self.state[self.actualized_unique_dims] = new_state_unique
        self.state[self.actualized_universal_dims] = new_state_universal

    def get_actualized_state(self):
        state_universal = self.state[self.actualized_unique_dims]
        state_unique = self.state[self.actualized_universal_dims]

        return np.concatenate([state_universal, state_unique], axis=0)
    
    def update_actualized_indxs(self, unique_indx=None, universal_indx=None):
        if unique_indx is not None:
            assert unique_indx.shape == self.actualized_unique_dims.shape
            self.actualized_unique_dims = unique_indx

        if universal_indx is not None:
            assert universal_indx.shape == self.actualized_universal_dims.shape
            self.actualized_universal_dims = universal_indx

    def get_state(self):
        return self.state
    
    def set_culture(self, culture_indx):
        self.culture_indx = culture_indx

