from copy import copy



class BaseConfig:
    def __init__(self, params:dict):
        dict(self.config, **params)
