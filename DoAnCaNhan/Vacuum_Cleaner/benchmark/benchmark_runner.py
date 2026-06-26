# =========================
# BENCHMARK RUNNER
# =========================
# File này dùng để chạy so sánh thuật toán và xuất dữ liệu ra file CSV.
# Mục tiêu:
# - Không làm thay đổi logic thuật toán gốc.
# - Chạy nhiều thuật toán trên cùng trạng thái để lấy số liệu công bằng hơn.
# - Dữ liệu CSV sau đó được dùng để vẽ biểu đồ trong báo cáo.
# - Bổ sung đo thời gian, số trạng thái đã thăm và bộ nhớ sử dụng.
# =========================

import copy
import csv
import os
import random
import time
import tracemalloc
from contextlib import contextmanager

from core.vacuum_problem import goal
from algorithms.algorithm_manager import solve
from algorithms.backtracking import mapcoloringbacktracking
from algorithms.forward_checking import forwardchecking
from algorithms.ac_3 import ac3search
from algorithms.min_conflicts import minconflicts
from algorithms.minimax import minimax
from algorithms.alpha_beta import alphabeta
from algorithms.expectimax import expectimax
from algorithms.caro_game import create_demo_board
from algorithms.partial_observation_search import partialobservationsearch


# =========================
# CẤU HÌNH OUTPUT
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "reports", "benchmark_data")
DEFAULT_OUTPUT_CSV = os.path.join(DEFAULT_OUTPUT_DIR, "benchmark_results.csv")


# =========================
# MAP MẪU CHO VACUUM CLEANER
# =========================
# Dùng các map 3x3 để thuật toán chạy nhanh, phù hợp demo trên lớp.
# Nếu dùng map quá lớn, BFS/UCS/IDS có thể duyệt rất nhiều trạng thái.
# =========================
VACUUM_TEST_MAPS = [
    (
        "vacuum_3x3_a",
        [
            [1, 1, 0],
            ["V", 1, 0],
            [0, 1, 1]
        ]
    ),
    (
        "vacuum_3x3_b",
        [
            ["V", 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
    ),
    (
        "vacuum_3x3_c",
        [
            [1, 0, 1],
            [0, "V", 1],
            [1, 0, 0]
        ]
    ),
    (
        "vacuum_3x3_d",
        [
            [0, 1, 1],
            [1, "V", 0],
            [0, 1, 1]
        ]
    ),
    (
        "vacuum_3x3_e",
        [
            ["V", 0, 1],
            [1, 1, 0],
            [1, 0, 1]
        ]
    )
]


# =========================
# THUẬT TOÁN CHẠY TRỰC TIẾP TRÊN VACUUM CLEANER
# =========================
VACUUM_SEARCH_ALGORITHMS = [
    ("Tìm kiếm không có thông tin", "BFS", "Dạng 1"),
    ("Tìm kiếm không có thông tin", "BFS", "Dạng 2"),
    ("Tìm kiếm không có thông tin", "DFS", "Dạng 1"),
    ("Tìm kiếm không có thông tin", "DFS", "Dạng 2"),
    ("Tìm kiếm không có thông tin", "IDS", "Dạng 1"),
    ("Tìm kiếm không có thông tin", "IDS", "Dạng 2"),
    ("Tìm kiếm không có thông tin", "UCS", "Dạng 1"),
    ("Tìm kiếm có thông tin", "Greedy", None),
    ("Tìm kiếm có thông tin", "A*", None),
    ("Tìm kiếm có thông tin", "IDA*", None),
]


LOCAL_SEARCH_ALGORITHMS = [
    "Simple Hill Climbing",
    "Steepest Ascent Hill Climbing",
    "Stochastic Hill Climbing",
    "Random Restart Hill Climbing",
    "Local Beam Search",
    "Simulated Annealing",
]


COMPLEX_ENVIRONMENT_ALGORITHMS = [
    "No Observation Search",
    "Partial Observation Search",
    "AND-OR Graph Search",
]


CSP_ALGORITHMS = [
    ("Backtracking", mapcoloringbacktracking),
    ("Forward Checking", forwardchecking),
    ("AC-3", ac3search),
    ("Min-Conflicts", lambda: minconflicts(max_steps=100, seed=42)),
]


ADVERSARIAL_ALGORITHMS = [
    ("Minimax", minimax),
    ("Alpha-Beta Pruning", alphabeta),
    ("Expectimax", expectimax),
]


ADVERSARIAL_TEST_BOARDS = [
    (
        "caro_demo_board",
        create_demo_board()
    ),
    (
        "caro_board_a",
        [
            ["X", "O", ""],
            ["", "X", ""],
            ["O", "", ""]
        ]
    ),
    (
        "caro_board_b",
        [
            ["O", "X", ""],
            ["", "X", ""],
            ["O", "", ""]
        ]
    ),
]


# =========================
# TẠO MAP NGẪU NHIÊN CÓ SEED
# =========================
# Dùng cho nhóm tìm kiếm cục bộ.
# Cùng một danh sách map được dùng cho mọi thuật toán để so sánh công bằng hơn.
# =========================
def create_seeded_floor(rows, cols, seed):
    rng = random.Random(seed)
    floor = []

    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(rng.choice([0, 1]))
        floor.append(row)

    vx = rng.randint(0, rows - 1)
    vy = rng.randint(0, cols - 1)
    floor[vx][vy] = "V"

    # Tránh trường hợp map quá dễ: không có ô bẩn nào.
    has_dirty = False
    for row in floor:
        for cell in row:
            if cell == 1:
                has_dirty = True
                break

    if not has_dirty:
        if vx == 0 and vy == 0:
            floor[rows - 1][cols - 1] = 1
        else:
            floor[0][0] = 1

    return floor


# =========================
# ĐẾM SỐ Ô BẨN CÒN LẠI
# =========================
def count_dirty_cells(floor):
    if floor is None:
        return ""

    # Belief state là list nhiều state.
    # Với benchmark chỉ cần tổng số ô bẩn còn lại trong tất cả state.
    if isinstance(floor, list) and len(floor) > 0 and isinstance(floor[0], list):
        if len(floor[0]) > 0 and isinstance(floor[0][0], list):
            total = 0
            for state in floor:
                total += count_dirty_cells(state)
            return total

    dirty = 0
    for row in floor:
        for cell in row:
            if cell == 1:
                dirty += 1

    return dirty


# =========================
# ĐO THỜI GIAN VÀ BỘ NHỚ
# =========================
def run_with_time_and_memory(function):
    tracemalloc.start()
    start_time = time.perf_counter()

    try:
        result = function()
        error = None
    except Exception as exc:
        result = None
        error = str(exc)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    runtime_ms = round((end_time - start_time) * 1000, 4)
    memory_kb = round(peak_memory / 1024, 4)

    return result, error, runtime_ms, memory_kb


# =========================
# ĐẾM NODE MỞ RỘNG
# =========================
@contextmanager
def count_vacuum_expansion_calls():
    counter = {
        "expanded_nodes": 0,
        "generated_nodes": 0
    }

    module_names = [
        "algorithms.bfs",
        "algorithms.dfs",
        "algorithms.ids",
        "algorithms.ucs",
        "algorithms.greedy_search",
        "algorithms.astar",
        "algorithms.idastar",
        "algorithms.simple_hill_climbing",
        "algorithms.steepest_ascent_hill_climbing",
        "algorithms.stochastic_hill_climbing",
        "algorithms.random_restart_hill_climbing",
        "algorithms.local_beam_search",
        "algorithms.simulated_annealing",
        "algorithms.no_observation_search",
        "algorithms.partial_observation_search",
        "algorithms.and_or_graph_search",
    ]

    originals = []

    try:
        for module_name in module_names:
            try:
                module = __import__(module_name, fromlist=["*"])
            except Exception:
                continue

            if hasattr(module, "get_possible_moves"):
                original_get_moves = getattr(module, "get_possible_moves")

                def wrapped_get_moves(floor, _original_get_moves=original_get_moves):
                    counter["expanded_nodes"] += 1
                    return _original_get_moves(floor)

                originals.append((module, "get_possible_moves", original_get_moves))
                setattr(module, "get_possible_moves", wrapped_get_moves)

            if hasattr(module, "move_vacuum"):
                original_move = getattr(module, "move_vacuum")

                def wrapped_move(floor, action, _original_move=original_move):
                    counter["generated_nodes"] += 1
                    return _original_move(floor, action)

                originals.append((module, "move_vacuum", original_move))
                setattr(module, "move_vacuum", wrapped_move)

        yield counter

    finally:
        for module, attr_name, original_value in originals:
            setattr(module, attr_name, original_value)


# =========================
# TẠO 1 DÒNG CSV RỖNG CHUẨN
# =========================
def create_empty_record():
    return {
        "group": "",
        "algorithm": "",
        "search_type": "",
        "problem": "",
        "case_id": "",
        "run_id": "",
        "depth": "",
        "success": "",
        "solution_steps": "",
        "expanded_nodes": "",
        "generated_nodes": "",
        "runtime_ms": "",
        "memory_kb": "",
        "final_dirty_cells": "",
        "assignments": "",
        "backtracks": "",
        "constraint_checks": "",
        "domain_reductions": "",
        "conflicts": "",
        "best_move": "",
        "best_score": "",
        "note": "",
    }


# =========================
# CHẠY 1 THUẬT TOÁN VACUUM
# =========================
def run_vacuum_algorithm(group_name, algorithm_name, search_type, floor, case_id, run_id=1):
    record = create_empty_record()
    record.update({
        "group": group_name,
        "algorithm": algorithm_name,
        "search_type": search_type or "",
        "problem": "Vacuum Cleaner",
        "case_id": case_id,
        "run_id": run_id,
    })

    with count_vacuum_expansion_calls() as counter:
        if search_type is None:
            call = lambda: solve(copy.deepcopy(floor), algorithm_name)
        else:
            call = lambda: solve(copy.deepcopy(floor), algorithm_name, search_type)

        result, error, runtime_ms, memory_kb = run_with_time_and_memory(call)

    record["runtime_ms"] = runtime_ms
    record["memory_kb"] = memory_kb
    record["expanded_nodes"] = counter["expanded_nodes"]
    record["generated_nodes"] = counter["generated_nodes"]

    if result is None:
        record["success"] = False
        record["note"] = error or "Không tìm thấy lời giải"
        return record

    path = result.get("path", [])
    final_state = path[-1] if len(path) > 0 else result.get("state")

    record["success"] = bool(final_state is not None and goal(final_state))
    record["solution_steps"] = max(len(path) - 1, 0) if len(path) > 0 else ""
    record["final_dirty_cells"] = count_dirty_cells(final_state)
    record["note"] = "OK"

    return record


# =========================
# CHẠY NHÓM VACUUM SEARCH
# =========================
def run_vacuum_search_benchmarks():
    records = []

    for case_id, floor in VACUUM_TEST_MAPS:
        for group_name, algorithm_name, search_type in VACUUM_SEARCH_ALGORITHMS:
            records.append(
                run_vacuum_algorithm(
                    group_name,
                    algorithm_name,
                    search_type,
                    floor,
                    case_id,
                    run_id=1
                )
            )

    return records


# =========================
# CHẠY NHÓM LOCAL SEARCH
# =========================
def run_local_search_benchmarks(run_count=10):
    records = []
    floors = []

    for run_id in range(1, run_count + 1):
        floors.append((run_id, create_seeded_floor(3, 3, seed=1000 + run_id)))

    for algorithm_name in LOCAL_SEARCH_ALGORITHMS:
        for run_id, floor in floors:
            records.append(
                run_vacuum_algorithm(
                    "Tìm kiếm cục bộ",
                    algorithm_name,
                    None,
                    floor,
                    "local_random_3x3",
                    run_id=run_id
                )
            )

    return records


# =========================
# CHẠY NHÓM MÔI TRƯỜNG PHỨC TẠP
# =========================
def create_partial_observation_data(floor):
    return {
        "actual_state": copy.deepcopy(floor),
        # Quan sát một vài ô cố định để benchmark ổn định.
        "observed_positions": [(0, 0), (1, 1), (2, 2)],
        "initial_belief_state": None,
    }


def run_complex_environment_algorithm(algorithm_name, floor, case_id, run_id=1):
    record = create_empty_record()
    record.update({
        "group": "Môi trường phức tạp",
        "algorithm": algorithm_name,
        "problem": "Belief State Vacuum Cleaner",
        "case_id": case_id,
        "run_id": run_id,
    })

    with count_vacuum_expansion_calls() as counter:
        if algorithm_name == "Partial Observation Search":
            data = create_partial_observation_data(floor)
            call = lambda: partialobservationsearch(data)
        else:
            call = lambda: solve(copy.deepcopy(floor), algorithm_name)

        result, error, runtime_ms, memory_kb = run_with_time_and_memory(call)

    record["runtime_ms"] = runtime_ms
    record["memory_kb"] = memory_kb
    record["expanded_nodes"] = counter["expanded_nodes"]
    record["generated_nodes"] = counter["generated_nodes"]

    if result is None:
        record["success"] = False
        record["note"] = error or "Không tìm thấy lời giải"
        return record

    path = result.get("path", [])
    final_state = path[-1] if len(path) > 0 else result.get("state")

    # Với belief state: dùng số ô bẩn còn lại để đánh giá kết quả cuối.
    final_dirty_cells = count_dirty_cells(final_state)

    record["success"] = final_dirty_cells == 0
    record["solution_steps"] = max(len(path) - 1, 0) if len(path) > 0 else ""
    record["final_dirty_cells"] = final_dirty_cells
    record["note"] = "OK"

    return record


def run_complex_environment_benchmarks():
    records = []

    for case_id, floor in VACUUM_TEST_MAPS:
        for algorithm_name in COMPLEX_ENVIRONMENT_ALGORITHMS:
            records.append(
                run_complex_environment_algorithm(
                    algorithm_name,
                    floor,
                    case_id,
                    run_id=1
                )
            )

    return records


# =========================
# ĐẾM METRIC TRONG STEP CSP
# =========================
def count_csp_metrics(steps):
    assignments = 0
    backtracks = 0
    domain_reductions = 0
    constraint_checks = len(steps)
    conflicts = 0

    for step in steps:
        step_type = step.get("type", "")

        if step_type == "assign":
            assignments += 1

        if step_type == "backtrack":
            backtracks += 1

        if step_type in ["forward_check", "revise", "remove", "domain_reduce"]:
            domain_reductions += 1

        if "conflicts" in step:
            step_conflicts = step.get("conflicts")
            if isinstance(step_conflicts, list):
                conflicts = len(step_conflicts)

    return assignments, backtracks, constraint_checks, domain_reductions, conflicts


# =========================
# CHẠY NHÓM CSP
# =========================
def run_csp_benchmarks(run_count=5):
    records = []

    for run_id in range(1, run_count + 1):
        for algorithm_name, function in CSP_ALGORITHMS:
            record = create_empty_record()
            record.update({
                "group": "Ràng buộc CSP",
                "algorithm": algorithm_name,
                "problem": "Map Coloring",
                "case_id": "tphcm_map",
                "run_id": run_id,
            })

            # Min-Conflicts có yếu tố ngẫu nhiên nên thay seed theo run_id.
            if algorithm_name == "Min-Conflicts":
                call = lambda run_id=run_id: minconflicts(max_steps=100, seed=42 + run_id)
            else:
                call = function

            result, error, runtime_ms, memory_kb = run_with_time_and_memory(call)
            record["runtime_ms"] = runtime_ms
            record["memory_kb"] = memory_kb

            if result is None:
                record["success"] = False
                record["note"] = error or "Không chạy được thuật toán CSP"
            else:
                steps = result.get("steps", [])
                assignments, backtracks, constraint_checks, domain_reductions, conflicts = count_csp_metrics(steps)

                record["success"] = result.get("success", False)
                record["assignments"] = assignments
                record["backtracks"] = backtracks
                record["constraint_checks"] = constraint_checks
                record["domain_reductions"] = domain_reductions
                record["conflicts"] = conflicts
                record["expanded_nodes"] = len(steps)
                record["generated_nodes"] = assignments + domain_reductions
                record["note"] = "OK"

            records.append(record)

    return records


# =========================
# CHẠY NHÓM ĐỐI KHÁNG
# =========================
def run_adversarial_benchmarks(max_depth=5):
    records = []

    for case_index, (case_id, board) in enumerate(ADVERSARIAL_TEST_BOARDS, start=1):
        for algorithm_name, function in ADVERSARIAL_ALGORITHMS:
            for depth in range(1, max_depth + 1):
                record = create_empty_record()
                record.update({
                    "group": "Đối kháng",
                    "algorithm": algorithm_name,
                    "problem": "TicTacToe",
                    "case_id": case_id,
                    "run_id": case_index,
                    "depth": depth,
                })

                call = lambda function=function, depth=depth, board=board: function(copy.deepcopy(board), max_depth=depth)
                result, error, runtime_ms, memory_kb = run_with_time_and_memory(call)

                record["runtime_ms"] = runtime_ms
                record["memory_kb"] = memory_kb

                if result is None:
                    record["success"] = False
                    record["note"] = error or "Không chạy được thuật toán đối kháng"
                else:
                    best_move = result.get("best_move")
                    if best_move is None:
                        best_move_text = ""
                    else:
                        best_move_text = f"({best_move[0] + 1},{best_move[1] + 1})"

                    expanded_nodes = result.get("expanded_nodes", "")

                    record["success"] = result.get("success", False)
                    record["expanded_nodes"] = expanded_nodes
                    record["generated_nodes"] = expanded_nodes
                    record["best_move"] = best_move_text
                    record["best_score"] = result.get("best_score", "")
                    record["note"] = "OK"

                records.append(record)

    return records


# =========================
# GHI CSV
# =========================
def write_records_to_csv(records, output_csv=DEFAULT_OUTPUT_CSV):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    fieldnames = list(create_empty_record().keys())

    with open(output_csv, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            writer.writerow(record)

    return output_csv


# =========================
# HÀM CHẠY TOÀN BỘ BENCHMARK
# =========================
def run_all_benchmarks(
    output_csv=DEFAULT_OUTPUT_CSV,
    local_run_count=10,
    csp_run_count=5,
    adversarial_max_depth=5
):
    records = []

    # Nhóm tìm kiếm cơ bản và có thông tin: chạy trên 5 map cố định.
    records.extend(run_vacuum_search_benchmarks())

    # Nhóm cục bộ: chạy 10 map random có seed để giảm yếu tố hên/xui.
    records.extend(run_local_search_benchmarks(run_count=local_run_count))

    # Nhóm môi trường phức tạp: chạy trên cùng 5 map với nhóm vacuum.
    records.extend(run_complex_environment_benchmarks())

    # CSP: chạy lặp 5 lần, riêng Min-Conflicts thay seed theo mỗi lần chạy.
    records.extend(run_csp_benchmarks(run_count=csp_run_count))

    # Đối kháng: chạy nhiều bàn cờ mẫu và nhiều độ sâu.
    records.extend(run_adversarial_benchmarks(max_depth=adversarial_max_depth))

    return write_records_to_csv(records, output_csv=output_csv)


# =========================
# CHẠY TRỰC TIẾP BẰNG TERMINAL
# =========================
if __name__ == "__main__":
    csv_path = run_all_benchmarks()
    print("Đã xuất benchmark:", csv_path)
