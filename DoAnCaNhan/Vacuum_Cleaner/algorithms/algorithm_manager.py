from algorithms.bfs import bfs_type1, bfs_type2
from algorithms.dfs import dfs_type1, dfs_type2
from algorithms.ids import ids_type1, ids_type2
from algorithms.ucs import ucs_type1

ALGORITHM_NAMES = [
    "BFS",
    "DFS",
    "IDS",
    "UCS"
]

SEARCH_TYPES = [
    "Dạng 1",
    "Dạng 2"
]


def get_algorithm_names():
    return ALGORITHM_NAMES


def get_search_types():
    return SEARCH_TYPES


def solve(initial_floor, algorithm_name, search_type="Dạng 1"):
    # search_type có mặc định "Dạng 1" để tránh lỗi nếu UI cũ gọi thiếu tham số

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
    
    raise ValueError(f"Chưa hỗ trợ thuật toán: {algorithm_name} - {search_type}")
