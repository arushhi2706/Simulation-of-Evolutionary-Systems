from dataclasses import dataclass

@dataclass
class Agent:
    id: int
    replication_rate: float = 0.04
    mutation_rate: float = 0.04
    death_rate: float = 0.02