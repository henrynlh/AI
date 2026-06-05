import random
import math

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
# SIMULATED ANNEALING
# =========================
# Ý tưởng:
# - Bắt đầu từ trạng thái ban đầu
# - T là nhiệt độ ban đầu
# - Khi T còn lớn hơn T_MIN thì tiếp tục lặp
# - Mỗi vòng lặp chọn ngẫu nhiên 1 trạng thái lân cận
# - Tính độ chênh lệch:
#   delta = h(next_state) - h(current_state)
# - Nếu delta < 0:
#   next_state tốt hơn current_state nên đi sang next_state
# - Ngược lại:
#   next_state xấu hơn nhưng vẫn có thể được chọn
#   với xác suất p = exp(-delta / T) <=> p=e^(-delta/T)
# - Sau mỗi vòng lặp, giảm nhiệt độ:
#   T = alpha * T
# - Nếu gặp goal thì trả về node hiện tại
# - Nếu nhiệt độ giảm xuống quá thấp mà chưa gặp goal
#   thì trả về current_node theo đúng mô tả thuật toán
# =========================
def simulatedannealing(initial_floor, t0=1000, t_min=0.01, alpha=0.95):
    current_node = {
        "state": initial_floor,
        "path": [initial_floor],
        "cost": count_wrong_cells(initial_floor)
    }

    # Khởi tạo nhiệt độ ban đầu
    T = t0

    while T > t_min:
        # Nếu trạng thái hiện tại là goal thì trả về
        if goal(current_node["state"]):
            return current_node

        actions = get_possible_moves(current_node["state"])

        # Chọn ngẫu nhiên 1 trạng thái lân cận
        action = random.choice(actions)
        next_state = move_vacuum(current_node["state"], action)

        current_cost = count_wrong_cells(current_node["state"])
        next_cost = count_wrong_cells(next_state)

        # delta = h(next_state) - h(current_state). 
        # Vì h(n) là số ô sai nên h càng nhỏ càng tốt
        delta = next_cost - current_cost

        # Nếu delta < 0 nghĩa là next_state tốt hơn current_state
        # Nếu trạng thái mới tốt hơn thì nhận luôn
        if delta < 0:
            current_node = {
                "state": next_state,
                "path": current_node["path"] + [next_state],
                "cost": next_cost
            }
        # Nếu trạng thái mới xấu hơn current_state
        # vẫn có thể nhận với xác suất p = exp(-delta / T)
        else:
            p = math.exp(-delta / T)

            # Sinh ngẫu nhiên số từ 0 đến 1
            # Nếu số đó nhỏ hơn p thì vẫn nhận trạng thái xấu hơn
            if random.random() < p:
                current_node = {
                    "state": next_state,
                    "path": current_node["path"] + [next_state],
                    "cost": next_cost
                }

        # Giảm nhiệt độ sau mỗi vòng lặp
        T = alpha * T

    # Khi T <= t_min mà chưa gặp goal
    # trả về trạng thái hiện tại mà thuật toán đang đứng
    return current_node
