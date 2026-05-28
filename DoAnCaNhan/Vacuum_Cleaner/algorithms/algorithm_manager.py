from algorithms.bfs import bfs_type1, bfs_type2
from algorithms.dfs import dfs_type1, dfs_type2
from algorithms.ids import ids_type1, ids_type2
from algorithms.ucs import ucs_type1
from algorithms.greedy_search import greedy
from algorithms.astar import astar


ALGORITHM_NAMES = [
    "BFS",
    "DFS",
    "IDS",
    "UCS",
    "Greedy",
    "A*"
]

SEARCH_TYPES = [
    "Dạng 1",
    "Dạng 2"
]

NO_TYPE_ALGORITHMS = [
    "Greedy",
    "A*"
]

def get_algorithm_names():
    return ALGORITHM_NAMES


def get_search_types():
    return SEARCH_TYPES


def get_no_type_algorithms():
    return NO_TYPE_ALGORITHMS


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

    raise ValueError(f"Chưa hỗ trợ thuật toán: {algorithm_name} - {search_type}")