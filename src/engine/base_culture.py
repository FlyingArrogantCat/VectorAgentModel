import numpy as np

from src.engine.base_agent import Agent


class Culture:
    def __init__(self, base, angle, num_max_actualized_dims, edu = None):
        self.base = np.array(base)
        self.angle = angle
        self.edu = edu
        self.num_max_actualized_dims = num_max_actualized_dims
    
    def angle_compute(self, state):
        return np.arccos(state @ self.base.T)

    def check_agent_in_culture(self, agent: Agent):
        agent_state = agent.get_state()

        angle = self.angle_compute(agent_state)
        condition = True if np.abs(angle) < self.angle else False

        return condition

    def check_vector_in_culture(self, agent_state):
        angle = self.angle_compute(agent_state)
        condition = True if np.abs(angle) < self.angle else False
        return condition
    
    def get_random_vector(self, lmbda=0.1):
        dim = self.base.shape[0]
        y = (self.base + np.random.normal(0, 0.2, dim)).reshape(self.base.shape[0], -1)
        x = (np.random.normal(0, 0.9) * np.cos(self.angle)) * y.T @ np.linalg.inv(y @ y.T + lmbda * np.eye(dim))
        while not self.check_vector_in_culture(x):
            x = (np.random.normal(0, 0.9) * np.cos(self.angle)) * y.T @ np.linalg.inv(y @ y.T + lmbda * np.eye(dim))
        # new_vec = np.random.normal(0, 1, self.base.shape[0])
        # while self.angle_compute(new_vec) < self.angle:
        #     new_vec = np.random.normal(0, 1, self.base.shape[0])
        #     new_vec /= np.linalg.norm(new_vec)
        return x[0, :]