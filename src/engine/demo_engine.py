import numpy as np
import scipy.spatial as sp

from src.engine.base_agent import Agent


class DemographyEngine():
    def __init__(self, args):
        self.config = args

    def process_birth(self, agent_set, culture_set):
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
            min_indx = np.argmin([np.linalg.norm(new_state - culture_set[agent_set[pair[0]].culture_indx].base),
                    np.linalg.norm(new_state - culture_set[agent_set[pair[1]].culture_indx].base)
                    ])
            culture_indx = agent_set[pair[int(min_indx)]].get_culture()
            
            actualized_unique_dims = np.array(
                            [ self.config["cultures"][culture_indx]["start_indx"] + 
                                self.config["universal_dim"] + x 
                                for x in range(culture_set[culture_indx].num_max_actualized_dims)])
            
            new_agent.update_actualized_unique_indxs(unique_indxes=actualized_unique_dims)
            new_agent.set_state(new_state)
            new_agent.set_culture(culture_indx)
            new_agent.init_probs()

            rand_value = np.random.uniform(0, 1, 1)
            if rand_value < self.config["birth_param"]:
                agent_set.append(new_agent)

    def process_death(self, agent_set, culture_set):
        indx_to_remove = []
        for indx, agent in enumerate(agent_set):
            rand_value = np.random.uniform(0, 1, 1)
            if rand_value < self.config["death_param"]:
                indx_to_remove.append(indx)

        for indx in sorted(indx_to_remove, reverse=True):
            del agent_set[indx]

    def process(self, agent_set, culture_set):
        
        self.process_birth(agent_set, culture_set)
        self.process_death(agent_set, culture_set)
        
        print(f"Agents: {len(agent_set)}")


