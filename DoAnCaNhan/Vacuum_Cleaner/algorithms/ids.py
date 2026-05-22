from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum,
    state_key
)


# =========================
# Kiểm tra state đã nằm trong path chưa
# Dùng để tránh bị lặp vòng trong DFS / IDS
# =========================
def in_path(state, path):
    key = state_key(state)

    for old_state in path:
        if state_key(old_state) == key:
            return True

    return False


# =========================
# DEPTH-LIMITED SEARCH DẠNG 1
# Lấy node ra khỏi frontier rồi mới kiểm tra goal
# =========================
def depth_limited_search_type1(initial_floor, limit):
    node = {
        "state": initial_floor,
        "path": [initial_floor],
        "depth": 0
    }

    frontier = []
    frontier.append(node)

    result = "failure"

    while len(frontier) > 0:
        node = frontier.pop()   # LIFO stack

        # Dạng 1: kiểm tra goal sau khi lấy node ra khỏi stack
        if goal(node["state"]):
            return node

        if node["depth"] >= limit:
            result = "cutoff"
        else:
            for action in get_possible_moves(node["state"]):
                child_state = move_vacuum(node["state"], action)

                if not in_path(child_state, node["path"]):
                    child = {
                        "state": child_state,
                        "path": node["path"] + [child_state],
                        "depth": node["depth"] + 1
                    }

                    frontier.append(child)

    return result


# =========================
# IDS DẠNG 1
# Gọi Depth-Limited Search với limit tăng dần
# =========================
def ids_type1(initial_floor):
    depth = 0

    while True:
        result = depth_limited_search_type1(initial_floor, depth)

        if result != "cutoff":
            return result

        depth += 1


# =========================
# DEPTH-LIMITED SEARCH DẠNG 2
# Vừa sinh child_state thì kiểm tra goal luôn
# =========================
def depth_limited_search_type2(initial_floor, limit):
    node = {
        "state": initial_floor,
        "path": [initial_floor],
        "depth": 0
    }

    # Kiểm tra riêng trạng thái ban đầu
    if goal(node["state"]):
        return node

    frontier = []
    frontier.append(node)

    result = "failure"

    while len(frontier) > 0:
        node = frontier.pop()   # LIFO stack

        if node["depth"] >= limit:
            result = "cutoff"
        else:
            for action in get_possible_moves(node["state"]):
                child_state = move_vacuum(node["state"], action)

                if not in_path(child_state, node["path"]):
                    child = {
                        "state": child_state,
                        "path": node["path"] + [child_state],
                        "depth": node["depth"] + 1
                    }

                    # Dạng 2: kiểm tra goal ngay khi sinh trạng thái con
                    if goal(child_state):
                        return child

                    frontier.append(child)

    return result


# =========================
# IDS DẠNG 2
# Gọi Depth-Limited Search với limit tăng dần
# =========================
def ids_type2(initial_floor):
    depth = 0

    while True:
        result = depth_limited_search_type2(initial_floor, depth)

        if result != "cutoff":
            return result

        depth += 1