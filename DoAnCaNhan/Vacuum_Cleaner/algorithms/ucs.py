from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum,
    state_key
)


# =========================
# Đếm số ô bẩn
# =========================
def count_dirty_cells(state):
    dirty = 0

    for row in state:
        for cell in row:
            if cell == 1:
                dirty += 1

    return dirty


# =========================
# Lấy node có cost nhỏ nhất trong frontier
# =========================
def pop_min_cost(frontier):
    min_index = 0

    for i in range(1, len(frontier)):
        if frontier[i]["cost"] < frontier[min_index]["cost"]:
            min_index = i

    return frontier.pop(min_index)


# =========================
# UCS DẠNG 1
# Lấy node có cost nhỏ nhất ra khỏi frontier
# rồi mới kiểm tra goal
# =========================
def ucs_type1(initial_floor):
    node = {
        "state": initial_floor,
        "path": [initial_floor],
        "cost": count_dirty_cells(initial_floor)
    }

    frontier = []
    frontier.append(node)

    reached = dict()
    reached[state_key(initial_floor)] = node["cost"]

    while len(frontier) > 0:
        # UCS: lấy node có cost nhỏ nhất
        node = pop_min_cost(frontier)

        key = state_key(node["state"])

        # Nếu node này không còn là đường đi tốt nhất tới state đó thì bỏ qua
        if node["cost"] > reached[key]:
            continue

        # Dạng 1: kiểm tra goal sau khi lấy node ra khỏi frontier
        if goal(node["state"]):
            return node

        for action in get_possible_moves(node["state"]):
            child_state = move_vacuum(node["state"], action)

            step_cost = count_dirty_cells(child_state)
            child_cost = node["cost"] + step_cost

            child = {
                "state": child_state,
                "path": node["path"] + [child_state],
                "cost": child_cost
            }

            child_key = state_key(child_state)

            if child_key not in reached or child_cost < reached[child_key]:
                reached[child_key] = child_cost
                frontier.append(child)

    return None