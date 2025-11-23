from agent import Agent
from utils import *
from constants import *
from constants import RANDOMNESS_FACTOR

class AgentManager:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.transition_vector = [self.agent.replication_rate, self.agent.mutation_rate, self.agent.death_rate, 1 - (self.agent.replication_rate + self.agent.mutation_rate + self.agent.death_rate)]
    
    def update_agent(self):
        return get_probabilistic_update_result([REPLICATE, MUTATE, DIE, NONE], self.transition_vector)
    
    def generate_mutated_agent(self, agent_id):
        mutated_agent = Agent(id=agent_id)
        mutated_agent.replication_rate = apply_noise(self.agent.replication_rate, RANDOMNESS_FACTOR)
        mutated_agent.mutation_rate = apply_noise(self.agent.mutation_rate, RANDOMNESS_FACTOR)
        mutated_agent.death_rate = apply_noise(self.agent.death_rate, RANDOMNESS_FACTOR)
        return mutated_agent