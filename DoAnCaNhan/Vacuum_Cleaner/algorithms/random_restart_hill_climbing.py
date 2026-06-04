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
# RANDOM RESTART HILL CLIMBING
# =========================
# Ý tưởng:
# - Chạy Hill Climbing nhiều lần, tối đa MAX_RESTART lần
# - Mỗi lượt bắt đầu lại từ trạng thái Start
# - Sinh tất cả trạng thái lân cận
# - Lọc ra các trạng thái tốt hơn current
# - Nếu không có trạng thái tốt hơn thì lượt này bị kẹt,
#   thoát vòng while và chuyển sang lượt restart tiếp theo
# - Nếu có, chọn trạng thái tốt nhất trong tập Better_Neighbors
# - Nếu tìm thấy goal thì trả về node hiện tại
# - Nếu chạy hết MAX_RESTART mà không tìm thấy goal thì trả về None
# =========================
def randomrestarthillclimbing(initial_floor, max_restart=10):
    for i in range(max_restart):
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
            # lượt này bị kẹt, nhảy sang lượt restart tiếp theo
            if len(better_neighbors) == 0:
                break

            # Chọn trạng thái tốt nhất trong tập Better_Neighbors
            best_cost = min(neighbor["cost"] for neighbor in better_neighbors)
            best_neighbors = []

            for neighbor in better_neighbors:
                if neighbor["cost"] == best_cost:
                    best_neighbors.append(neighbor)

            # Nếu có nhiều trạng thái cùng tốt nhất thì chọn ngẫu nhiên 1 trạng thái
            next_neighbor = random.choice(best_neighbors)

            current_node = {
                "state": next_neighbor["state"],
                "path": current_node["path"] + [next_neighbor["state"]],
                "cost": next_neighbor["cost"]
            }

    # Chạy hết max_restart lượt mà không chạm được goal
    return None
 