from algorithms.bfs import bfs_type1, bfs_type2
from algorithms.dfs import dfs_type1, dfs_type2
from algorithms.ids import ids_type1, ids_type2
from algorithms.ucs import ucs_type1
from algorithms.greedy_search import greedy
from algorithms.astar import astar
from algorithms.idastar import idastar
from algorithms.simple_hill_climbing import simplehillclimbing
from algorithms.steepest_ascent_hill_climbing import steepestascenthillclimbing
from algorithms.stochastic_hill_climbing import stochastichillclimbing
from algorithms.random_restart_hill_climbing import randomrestarthillclimbing
from algorithms.local_beam_search import localbeamsearch
from algorithms.simulated_annealing import simulatedannealing
from algorithms.no_observation_search import noobservationastar
from algorithms.partial_observation_search import partialobservationsearch

ALGORITHM_NAMES = [
    "BFS",
    "DFS",
    "IDS",
    "UCS",
    "Greedy",
    "A*",
    "IDA*",
    "Simple Hill Climbing",
    "Steepest Ascent Hill Climbing",
    "Stochastic Hill Climbing",
    "Random Restart Hill Climbing",
    "Local Beam Search",
    "Simulated Annealing",
    "No Observation Search",
    "Partial Observation Search"
]

SEARCH_TYPES = [
    "Dạng 1",
    "Dạng 2"
]

NO_TYPE_ALGORITHMS = [
    "Greedy",
    "A*",
    "IDA*",
    "Simple Hill Climbing",
    "Steepest Ascent Hill Climbing",
    "Stochastic Hill Climbing",
    "Random Restart Hill Climbing",
    "Local Beam Search",
    "Simulated Annealing",
    "No Observation Search",
    "Partial Observation Search"
]

ONE_TYPE_ALGORITHMS = [
    "UCS"
]

def get_algorithm_names():
    return ALGORITHM_NAMES

def get_search_types():
    return SEARCH_TYPES

def get_no_type_algorithms():
    return NO_TYPE_ALGORITHMS

def get_one_type_algorithms():
    return ONE_TYPE_ALGORITHMS


def solve(initial_floor, algorithm_name, search_type="Dạng 1"):
    if algorithm_name == "BFS" and search_type == "Dạng 1":
        return bfs_type1(initial_floor)

    if algorithm_name == "BFS" and search_type == "Dạng 2":
        return bfs_type2(initial_floor)

    if algorithm_name == "DFS" and search_type == "Dạng 1":
        return dfs_type1(initial_floor)

    if algorithm_name == "DFS" and search_type == "Dạng 2":
        return dfs_type2(initial_floor)

    if algorithm_name == "IDS" and search_type == "Dạng 1":
        return ids_type1(initial_floor)

    if algorithm_name == "IDS" and search_type == "Dạng 2":
        return ids_type2(initial_floor)

    if algorithm_name == "UCS" and search_type == "Dạng 1":
        return ucs_type1(initial_floor)

    # Các thuật toán không chia Dạng 1 / Dạng 2
    if algorithm_name == "Greedy":
        return greedy(initial_floor)

    if algorithm_name == "A*":
        return astar(initial_floor)
    
    if algorithm_name == "IDA*":
        return idastar(initial_floor)
    
    if algorithm_name == "Simple Hill Climbing":
        return simplehillclimbing(initial_floor)
    
    if algorithm_name == "Steepest Ascent Hill Climbing":
        return steepestascenthillclimbing(initial_floor)
    
    if algorithm_name == "Stochastic Hill Climbing":
        return stochastichillclimbing(initial_floor)
    
    if algorithm_name == "Random Restart Hill Climbing":
        return randomrestarthillclimbing(initial_floor)
    
    if algorithm_name == "Local Beam Search":
        return localbeamsearch(initial_floor)
    
    if algorithm_name == "Simulated Annealing":
        return simulatedannealing(initial_floor)
        
    if algorithm_name == "No Observation Search":
        return noobservationastar(initial_floor)

    if algorithm_name == "Partial Observation Search":
        return partialobservationsearch(initial_floor)

    raise ValueError(f"Chưa hỗ trợ thuật toán: {algorithm_name} - {search_type}")