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
from algorithms.and_or_graph_search import andorgraphsearch
from algorithms.minimax import minimax
from algorithms.alpha_beta import alphabeta
from algorithms.expectimax import expectimax


# =========================
# DANH SÁCH THUẬT TOÁN THEO NHÓM
# =========================
UNINFORMED_ALGORITHMS = [
    "BFS",
    "DFS",
    "IDS",
    "UCS"
]

INFORMED_ALGORITHMS = [
    "Greedy",
    "A*",
    "IDA*"
]

LOCAL_SEARCH_ALGORITHMS = [
    "Simple Hill Climbing",
    "Steepest Ascent Hill Climbing",
    "Stochastic Hill Climbing",
    "Random Restart Hill Climbing",
    "Local Beam Search",
    "Simulated Annealing"
]

COMPLEX_ENVIRONMENT_ALGORITHMS = [
    "No Observation Search",
    "Partial Observation Search",
    "AND-OR Graph Search"
]

CSP_ALGORITHMS = [
    "Map Coloring Backtracking",
    "Forward Checking",
    "AC-3",
    "Min-Conflicts"
]

ADVERSARIAL_ALGORITHMS = [
    "Minimax",
    "Alpha-Beta Pruning",
    "Expectimax"
]

ALGORITHM_GROUPS = {
    "Tìm kiếm không có thông tin": UNINFORMED_ALGORITHMS,
    "Tìm kiếm có thông tin": INFORMED_ALGORITHMS,
    "Tìm kiếm cục bộ": LOCAL_SEARCH_ALGORITHMS,
    "Môi trường phức tạp": COMPLEX_ENVIRONMENT_ALGORITHMS,
    "Ràng buộc CSP": CSP_ALGORITHMS,
    "Đối kháng": ADVERSARIAL_ALGORITHMS
}

ALGORITHM_NAMES = []
for group_algorithms in ALGORITHM_GROUPS.values():
    ALGORITHM_NAMES.extend(group_algorithms)

SEARCH_TYPES = [
    "Dạng 1",
    "Dạng 2"
]

# Các thuật toán không chia Dạng 1 / Dạng 2.
NO_TYPE_ALGORITHMS = (
    INFORMED_ALGORITHMS
    + LOCAL_SEARCH_ALGORITHMS
    + COMPLEX_ENVIRONMENT_ALGORITHMS
    + CSP_ALGORITHMS
    + ADVERSARIAL_ALGORITHMS
)

# UCS trong project hiện chỉ cài Dạng 1.
ONE_TYPE_ALGORITHMS = [
    "UCS"
]

# =========================
# HÀM GETTER CHO UI
# =========================
def get_algorithm_names():
    return ALGORITHM_NAMES


def get_algorithm_groups():
    return ALGORITHM_GROUPS


def get_search_types():
    return SEARCH_TYPES


def get_no_type_algorithms():
    return NO_TYPE_ALGORITHMS


def get_one_type_algorithms():
    return ONE_TYPE_ALGORITHMS


def get_csp_algorithms():
    return CSP_ALGORITHMS


def get_adversarial_algorithms():
    return ADVERSARIAL_ALGORITHMS


def get_complex_environment_algorithms():
    return COMPLEX_ENVIRONMENT_ALGORITHMS


# =========================
# HÀM SOLVE TRUNG TÂM
# =========================
# initial_floor:
# - Với nhóm Vacuum Cleaner: là ma trận sàn nhà.
# - Với nhóm đối kháng: được hiểu là board caro 3x3.
#
# Các nhóm có visualizer riêng như CSP và đối kháng thường được mở trực tiếp
# từ UI. 
# =========================
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

    # =========================
    # TÌM KIẾM CÓ THÔNG TIN
    # =========================
    if algorithm_name == "Greedy":
        return greedy(initial_floor)

    if algorithm_name == "A*":
        return astar(initial_floor)

    if algorithm_name == "IDA*":
        return idastar(initial_floor)

    # =========================
    # TÌM KIẾM CỤC BỘ
    # =========================
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

    # =========================
    # MÔI TRƯỜNG PHỨC TẠP
    # =========================
    if algorithm_name == "No Observation Search":
        return noobservationastar(initial_floor)

    if algorithm_name == "Partial Observation Search":
        return partialobservationsearch(initial_floor)

    if algorithm_name == "AND-OR Graph Search":
        return andorgraphsearch(initial_floor)

    # =========================
    # NHÓM ĐỐI KHÁNG
    # =========================
    if algorithm_name == "Minimax":
        return minimax(initial_floor)

    if algorithm_name == "Alpha-Beta Pruning":
        return alphabeta(initial_floor)

    if algorithm_name == "Expectimax":
        return expectimax(initial_floor)

    raise ValueError(f"Chưa hỗ trợ thuật toán: {algorithm_name} - {search_type}")
