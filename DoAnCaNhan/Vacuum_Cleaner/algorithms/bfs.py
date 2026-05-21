from collections import deque

from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum,
    state_key
)


# =========================
# BFS DẠNG 1
# Lấy node ra khỏi frontier rồi mới kiểm tra goal
# =========================
def bfs_type1(initial_floor):
    node = {
        "state": initial_floor,
        "path": [initial_floor]
    }

    frontier = deque()
    frontier.append(node)

    reached = set()
    reached.add(state_key(initial_floor))

    while len(frontier) > 0:
        node = frontier.popleft()

        # Dạng 1: kiểm tra goal sau khi lấy node ra khỏi queue
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
# BFS DẠNG 2
# Vừa sinh child_state thì kiểm tra goal luôn
# =========================
def bfs_type2(initial_floor):
    node = {
        "state": initial_floor,
        "path": [initial_floor]
    }

    # Kiểm tra riêng trạng thái ban đầu
    if goal(node["state"]):
        return node

    frontier = deque()
    frontier.append(node)

    reached = set()
    reached.add(state_key(initial_floor))

    while len(frontier) > 0:
        node = frontier.popleft()

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
