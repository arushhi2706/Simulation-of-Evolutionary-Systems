import random
from constants import *

def apply_noise(value, noise_percentage):
    return value * (1 + random.uniform(-noise_percentage, noise_percentage))

def get_probabilistic_update_result(actions, probs):
    return random.choices(actions, probs)[0]

def get_base_agent_spawn_result():
    spawn_result = get_probabilistic_update_result([SPAWN, NONE], [BASIC_AGENT_SPAWN_RATE, 1 - BASIC_AGENT_SPAWN_RATE])
    if (spawn_result == SPAWN):
        return 1
    return 0