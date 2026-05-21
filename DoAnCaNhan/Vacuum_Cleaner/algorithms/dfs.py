from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum,
    state_key
)


# =========================
# DFS DẠNG 1
# Lấy node ra khỏi frontier rồi mới kiểm tra goal
# =========================
def dfs_type1(initial_floor):
    node = {
        "state": initial_floor,
        "path": [initial_floor]
    }

    frontier = []
    frontier.append(node)

    reached = set()
    reached.add(state_key(initial_floor))

    while len(frontier) > 0:
        node = frontier.pop()

        # Dạng 1: kiểm tra goal sau khi lấy node ra khỏi stack
        if goal(node["state"]):
            return node

        for action in get_possible_moves(node["state"]):
            child_state = move_vacuum(node["state"], action)

            child = {
                "state": child_state,
                "path": node["path"] + [child_state]
            }

            if state_key(child_state) not in reached:
                reached.add(state_key(child_state))
                frontier.append(child)

    return None


# =========================
# DFS DẠNG 2
# Vừa sinh child_state thì kiểm tra goal luôn
# =========================
def dfs_type2(initial_floor):
    node = {
        "state": initial_floor,
        "path": [initial_floor]
    }

    # Kiểm tra riêng trạng thái ban đầu
    if goal(node["state"]):
        return node

    frontier = []
    frontier.append(node)

    reached = set()
    reached.add(state_key(initial_floor))

    while len(frontier) > 0:
        node = frontier.pop()

        for action in get_possible_moves(node["state"]):
            child_state = move_vacuum(node["state"], action)

            child = {
                "state": child_state,
                "path": node["path"] + [child_state]
            }

            if state_key(child_state) not in reached:

                # Dạng 2: kiểm tra goal ngay khi sinh trạng thái con
                if goal(child_state):
                    return child

                reached.add(state_key(child_state))
                frontier.append(child)

    return None
