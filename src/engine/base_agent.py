import numpy as np


class BaseAgent:
    def __init__(self, dim, state=None):
        self.dim = dim

        self.state = np.zeros(dim) if state is None else state

    def state_update(self, new_state):

        self.state = new_state

    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state


class Agent(BaseAgent):
    def __init__(self, dim_unique:int, dim_universal:int):
        dim = dim_unique + dim_universal
        super(Agent, self).__init__(dim=dim)
        assert dim == dim_unique + dim_universal, f"Incorrect input {dim}"

        self.dim_unique = dim_unique
        self.dim_universal = dim_universal

        self.actualized_universal_dims = np.arange(0, dim_universal)
        self.actualized_unique_dims = np.arange(dim_universal, dim_universal + dim_unique)

        self.culture_indx = 0
        self.num_max_actualized_dims = dim_unique

        self.probabilities = None

    def init_probs(self):
        self.probabilities = self.state / np.linalg.norm(self.state)

    def update_state(self, new_state_unique, new_state_universal):
        self.state[self.actualized_unique_dims] = new_state_unique
        self.state[self.actualized_universal_dims] = new_state_universal

    def get_actualized_states(self):
        state_universal = self.state[self.actualized_universal_dims]
        state_unique = self.state[self.actualized_unique_dims]
        return np.concatenate([state_universal, state_unique], axis=0)
    
    def get_actualized_universal_state(self):
        state_universal = self.state[self.actualized_universal_dims]
        return state_universal
    
    def get_actualized_unique_state(self):
        state_unique = self.state[self.actualized_unique_dims]
        return state_unique
    
    def update_actualized_unique_indxs(self, unique_indxes):
        assert max(unique_indxes) <= self.dim_unique + self.dim_universal
        self.actualized_unique_dims = unique_indxes

    def set_actualized_universal_state(self, new_state):
        assert new_state.shape == self.state[self.actualized_universal_dims].shape
        self.state[self.actualized_universal_dims] = new_state
    
    def set_actualized_unique_state(self, new_state):
        assert new_state.shape == self.state[self.actualized_unique_dims].shape
        self.state[self.actualized_unique_dims] = new_state

    def set_culture(self, culture_indx):
        self.culture_indx = culture_indx

    def get_culture(self):
        return self.culture_indx
