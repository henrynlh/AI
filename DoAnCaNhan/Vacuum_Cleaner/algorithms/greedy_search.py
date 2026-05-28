from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum,
    state_key,
    find_vacuum
)


# =========================
# Tính khoảng cách Manhattan
# =========================
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# =========================
# Heuristic cho Greedy
# Cost = khoảng cách Manhattan
# từ máy hút bụi tới ô bẩn gần nhất
# =========================
def manhattan_cost(state):
    vacuum_pos = find_vacuum(state)

    if vacuum_pos is None:
        return 0

    min_distance = None

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 1:
                dirty_pos = (i, j)
                distance = manhattan_distance(vacuum_pos, dirty_pos)

                if min_distance is None or distance < min_distance:
                    min_distance = distance

    # Nếu không còn ô bẩn thì cost = 0
    if min_distance is None:
        return 0

    return min_distance


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
# GREEDY BEST-FIRST SEARCH
# Cost = heuristic Manhattan
# =========================
def greedy(initial_floor):
    node = {
        "state": initial_floor,
        "path": [initial_floor],
        "cost": manhattan_cost(initial_floor)
    }

    frontier = []
    frontier.append(node)

    reached = set()
    reached.add(state_key(initial_floor))

    while len(frontier) > 0:
        # Greedy: lấy node có heuristic nhỏ nhất
        node = pop_min_cost(frontier)

        # Kiểm tra goal sau khi lấy node ra khỏi frontier
        if goal(node["state"]):
            return node

        for action in get_possible_moves(node["state"]):
            child_state = move_vacuum(node["state"], action)
            child_key = state_key(child_state)

            if child_key not in reached:
                child = {
                    "state": child_state,
                    "path": node["path"] + [child_state],
                    "cost": manhattan_cost(child_state)
                }

                reached.add(child_key)
                frontier.append(child)

    return None