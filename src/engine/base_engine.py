import numpy as np
import json 

from src.engine.base_agent import Agent
from src.engine.base_culture import Culture
from src.engine.edu_engine import EducationalEngine
from src.engine.demo_engine import DemographyEngine


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
        num_max_actualized_dims_s = np.array([x["num_max_actualized_dims"] for x in self.config["cultures"]])
        edu = [None for _ in bases]
        self.cultures_initialization(bases, 
                                     angles=angles, 
                                     num_max_actualized_dims_s=num_max_actualized_dims_s, 
                                     edus=edu)
        agents_number = [x["amount"] for x in self.config["cultures"]]
        self.agent_initialization(agents_number)

    def cultures_initialization(self, bases, angles, num_max_actualized_dims_s, edus=None):
        for base, \
            angle, \
            num_max_actualized_dims, \
            edu in zip(bases, angles, num_max_actualized_dims_s, edus):

            self.cultures.append(Culture(base, 
                                         angle=angle, 
                                         num_max_actualized_dims=num_max_actualized_dims, 
                                         edu=edu))

    def agent_initialization(self, agents_number):
        assert len(agents_number) == len(self.cultures)
        for indx, culture, agent_n in zip(np.arange(0, len(self.cultures)), self.cultures, agents_number):
            for _ in range(agent_n):
                agent = Agent(self.config["unique_dim"], 
                              self.config["universal_dim"])

                #actualized_universal_dims = np.array([x for x in range(self.config["universal_dim"])])
                actualized_unique_dims = np.array(
                                            [ self.config["cultures"][indx]["start_indx"] + 
                                              self.config["universal_dim"] + x 
                                              for x in range(culture.num_max_actualized_dims)])
                
                agent.update_actualized_unique_indxs(unique_indxes=actualized_unique_dims)
                agent.set_state(culture.get_random_vector(self.config["seed"]))
                agent.set_culture(culture_indx=indx)
                agent.init_probs()
                self.agents_set.append(agent)

    def start(self):
        for indx in range(self.config["num_steps"]):
            self.procees_one_step(self.config["speed"])

    def procees_one_step(self, speed: float):
        self.process_universal_states(speed)
        self.process_unique_states(speed)

        self.educational_engine.process(self.agents_set)

        self.demography_engine.process()


    def process_unique_states(self, speed: float):
        probs = np.array([agent.probabilities for agent in self.agents_set])

        agents_num = probs.shape[0]
        dims = probs.shape[0]

        deriv = np.zeros_like(probs)
        for agent_indx in range(agents_num):
            for dim in range(dims):
                deriv[agent_indx, dim] = self.config["lambda"] * (probs[:, dim] - probs[agent_indx, dim]) \
                                         + (1 - self.config["lambda"]) * probs[agent_indx, dim]
        
        probs = probs + speed * deriv

        for agent_indx in range(agents_num):
            self.agents_set[agent_indx].probabilities = probs[agent_indx] / np.linalg.norm(probs[agent_indx])


    def process_universal_states(self, speed: float):
        mean = [agent.get_actualized_universal_state() for agent in self.agents_set]
        mean = np.mean(mean, axis=0)
        for agent in self.agents_set:
            agent_state = agent.get_actualized_universal_state() * (1 - speed) + speed * mean
            agent.set_actualized_universal_state(agent_state)


    def dims_actualization(self):
        pass