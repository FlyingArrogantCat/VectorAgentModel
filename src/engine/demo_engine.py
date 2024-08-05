import numpy as np
import scipy.spatial as sp

from src.engine.base_agent import Agent


class DemographyEngine():
    def __init__(self, args):
        self.config = args

    def process(self, agent_set, culture_set):
        pairs = []
        nonselected_indxes = np.arange(len(agent_set))
        selected_indxes = []
        actualized_states = np.array([agent.get_unique_state() for agent in agent_set])

        dist = sp.distance_matrix(actualized_states, actualized_states)
        for indx in range(len(agent_set)):
            dist[indx, indx] = 10e6
        for indx in range(len(agent_set)):
            if indx in selected_indxes:
                continue
            min_indx = np.argmin(dist[indx, nonselected_indxes])
            np.delete(nonselected_indxes, min_indx)
            np.delete(nonselected_indxes, indx)
            selected_indxes.append(indx)
            selected_indxes.append(min_indx)
            pairs.append([indx, min_indx])

        for pair in pairs:
            new_state = (agent_set[pair[0]].state + agent_set[pair[1]].state) / 2
            new_agent = Agent(dim_universal=agent_set[pair[0]].dim_universal, 
                              dim_unique=agent_set[pair[0]].dim_unique)
            new_agent.set_state(new_state)

            min_indx = np.argmin([np.linalg.norm(new_state - culture_set[agent_set[pair[0]].culture_indx].base),
                                np.linalg.norm(new_state - culture_set[agent_set[pair[1]].culture_indx].base)
                                ])

            new_agent.set_culture(agent_set[pair[int(min_indx)]])
