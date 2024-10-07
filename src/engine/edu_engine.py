import numpy as np
import json 


class EducationalEngine():
    def __init__(self, args):
        self.config = args

        self.educational_states = np.array([culture["edu"] for culture in self.config["cultures"]])
        self.speed = self.config["edu_speed"]#self.config["speed"]

    def process(self, agents_set):
        for agent in agents_set:
            state = self.educational_states[agent.get_culture()]
            agent.probabilities = agent.probabilities * (1 - self.speed) + self.speed * state
            agent.probabilities = agent.probabilities / np.linalg.norm(agent.probabilities)
