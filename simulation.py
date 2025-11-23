import matplotlib.pyplot as plt
from utils import *
from constants import *
from agent import Agent
from agent_manager import AgentManager

class Simulation:
    def __init__(self, timesteps):
        self.timesteps = timesteps
        self.state = SIM_START_STATE
        self.num_unique_agents = len(SIM_START_STATE)
    
    def run(self):
        plt.ion()
        fig, ax = plt.subplots()
        
        history, spawn_timestep = {}, {}
        
        for timestep in range(self.timesteps):
            print(f"Timestep {timestep}")
            total_agents = 0
            
            for agent_id, info in self.state.items():
                total_agents += info[COUNT]
                if agent_id in history.keys():
                    history[agent_id].append(info[COUNT])
                else:
                    history[agent_id] = [info[COUNT]]
                    spawn_timestep[agent_id] = timestep
            print(f"Total number of agents: {total_agents}")
            
            ax.clear()
            for agent_id, counts in history.items():
                start = spawn_timestep[agent_id]
                x_values = list(range(start, start + len(counts)))
                ax.plot(x_values, counts, label=f"Agent {agent_id}")
            ax.legend()
            ax.set_xlabel("Timestep")
            ax.set_ylabel("Agent Count")
            ax.set_title("Agent Counts Over Time")
            plt.pause(0.05)
            
            self.update_state()
        
        plt.ioff()
        plt.show()
    
    def update_state(self):
        base_agent_spawn = get_base_agent_spawn_result()
        if (base_agent_spawn):
            print("Agent 0 spawned!")
        
        new_state = self.get_update_existing_state_result()
        new_state[0][COUNT] += base_agent_spawn
        self.state = new_state
    
    def get_update_existing_state_result(self):
        new_state = self.state.copy()
        
        for agent_id, info in self.state.items():
            agent_info = info[AGENT]
            agent_manager = AgentManager(agent=Agent(id=agent_id, replication_rate=agent_info[REPLICATE], mutation_rate=agent_info[MUTATE], death_rate=agent_info[DIE]))
            
            for _ in range(info[COUNT]):
                update_agent_result = agent_manager.update_agent()
                
                if (update_agent_result == REPLICATE):
                    print(f"Agent {agent_id} replicated!")
                    new_state[agent_id][COUNT] += 1
                
                elif (update_agent_result == MUTATE):
                    print(f"Agent {agent_id} mutated!")
                    new_state[agent_id][COUNT] -= 1
                    mutated_agent = agent_manager.generate_mutated_agent(self.num_unique_agents)
                    equivalent_agent_id = self.is_mutated_agent_unique(mutated_agent)
                    if (equivalent_agent_id < 0):
                        new_state[self.num_unique_agents] = {
                                AGENT: {
                                    REPLICATE: mutated_agent.replication_rate,
                                    MUTATE: mutated_agent.mutation_rate,
                                    DIE: mutated_agent.death_rate
                                },
                                COUNT: 1
                            }
                        self.num_unique_agents += 1
                    else:
                        new_state[equivalent_agent_id][COUNT] += 1
                
                elif (update_agent_result == DIE):
                    print(f"Agent {agent_id} died :(")
                    new_state[agent_id][COUNT] -= 1
        
        return new_state
    
    def is_mutated_agent_unique(self, mutated_agent):
        for id, info in self.state.items():
            agent_info = info[AGENT]
            if (mutated_agent.replication_rate == agent_info[REPLICATE] and mutated_agent.mutation_rate == agent_info[MUTATE] and mutated_agent.death_rate == agent_info[DIE]):
                return id
        return -1


if __name__ == "__main__":
    sim = Simulation(500)
    sim.run()