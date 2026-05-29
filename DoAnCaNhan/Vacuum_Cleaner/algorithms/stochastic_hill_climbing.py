import random

from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum
)


# =========================
# h(n): số ô sai
# Với bài máy hút bụi:
# số ô sai = số ô bẩn còn lại
# =========================
def count_wrong_cells(state):
    wrong = 0

    for row in state:
        for cell in row:
            if cell == 1:
                wrong += 1

    return wrong


# =========================
# STOCHASTIC HILL CLIMBING
# =========================
# Ý tưởng:
# - Bắt đầu từ trạng thái ban đầu
# - Sinh tất cả trạng thái lân cận
# - Lọc ra các trạng thái tốt hơn current
# - Nếu không có trạng thái tốt hơn thì dừng
# - Nếu có, chọn ngẫu nhiên 1 trạng thái tốt hơn để đi tiếp
# =========================
def stochastichillclimbing(initial_floor):
    current_node = {
        "state": initial_floor,
        "path": [initial_floor],
        "cost": count_wrong_cells(initial_floor)
    }

    while True:
        # Nếu trạng thái hiện tại là goal thì trả về
        if goal(current_node["state"]):
            return current_node

        current_cost = count_wrong_cells(current_node["state"])

        better_neighbors = []

        # Sinh tất cả trạng thái lân cận
        for action in get_possible_moves(current_node["state"]):
            next_state = move_vacuum(current_node["state"], action)
            next_cost = count_wrong_cells(next_state)

            # Vì h(n) là số ô sai nên h càng nhỏ càng tốt
            # Lọc các trạng thái tốt hơn current
            if next_cost < current_cost:
                neighbor = {
                    "state": next_state,
                    "cost": next_cost
                }

                better_neighbors.append(neighbor)

        # Nếu không có trạng thái tốt hơn
        # và hiện tại chưa phải goal thì xem như không tìm thấy lời giải
        if len(better_neighbors) == 0:
            return None

        # Chọn ngẫu nhiên 1 trạng thái tốt hơn
        next_neighbor = random.choice(better_neighbors)

        current_node = {
            "state": next_neighbor["state"],
            "path": current_node["path"] + [next_neighbor["state"]],
            "cost": next_neighbor["cost"]
        }