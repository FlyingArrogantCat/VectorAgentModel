import numpy as np
import json 

from src.engine.base_agent import Agent
from src.engine.base_culture import Culture


class DemographyEngine():
    def __init__(self, args):
        pass

    def process(self):
        pass


class EducationalEngine():
    def __init__(self, args):
        pass

    def process(self):
        pass


class Engine(object):
    def __init__(self, args):
        self.cultures = []
        self.agents_set = []

        self.args = args
        with open(self.args.config, "r") as file:
            self.config = json.loads(file.read())

        self.demography_engine = DemographyEngine(self.config)
        self.educational_engine = EducationalEngine(self.config)

        self.cultures_number = self.config["cultures_number"]

        bases = np.array([x["base"] for x in self.config["cultures"]])
        angles = np.array([x["angle"] for x in self.config["cultures"]])
        edu = [None for _ in bases]

        self.cultures_initialization(bases, angles=angles, edus=edu)

        agents_number = [x["amount"] for x in self.config["cultures"]]
        self.agent_initialization(agents_number)


    def cultures_initialization(self, bases, angles, edus=None):
        for base, angle, edu in zip(bases, angles, edus):
            self.cultures.append(Culture(base, angle=angle, edu=edu))


    def agent_initialization(self, agents_number):
        assert len(agents_number) == len(self.cultures)
        for culture, agent_n in zip(self.cultures, agents_number):
            for _ in range(agent_n):
                agent = Agent(self.config["total_dim"], self.config["unique_dim"], self.config["universal_dim"])
                agent.set_state(culture.get_random_vector(0.05))
                self.agents_set.append(agent)


    def start(self):
        for indx in range(self.config["num_steps"]):
            self.procees_one_step()


    def procees_one_step(self, speed: float = 1e-5):
        
        self.process_universal_states(speed)

        self.process_unique_states(speed)


        self.demography_engine.process()

        self.educational_engine.process()


    def process_unique_states(self, speed: float):
        pass

    def process_universal_states(self, speed: float):
        mean = np.zeros()


    def dims_actualization(self):
        pass