
from src.engine.base_agent import Agent
from src.engine.base_culture import Culture


class DemographyEngine():
    def __init__(self, args):
        pass


class EducationalEngine():
    def __init__(self, args):
        pass


class Engine(object):
    def __init__(self, args):
        self.args = args
    
        self.cultures_number = args.cultures_number

        self.cultures = [Culture()]

        self.agents_set = [Agent()]


    def agent_initialization(self):
        pass

    def start(self):
        pass


    def procees_one_step(self, speed: float):
        pass
