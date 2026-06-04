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
# Chuyển state sang dạng có thể lưu trong set
# Mục đích:
# - Tránh sinh trùng trạng thái
# - Tránh lặp vô hạn khi các trạng thái quay lại nhau
# =========================
def state_to_key(state):
    return tuple(tuple(row) for row in state)


# =========================
# Sinh ngẫu nhiên 1 trạng thái từ Start
# Cách làm:
# - Bắt đầu từ initial_floor
# - Đi ngẫu nhiên một số bước
# - Trạng thái nhận được xem như 1 trạng thái khởi tạo trong beam
# =========================
def random_state_from_start(initial_floor, max_random_steps):
    current_state = initial_floor
    path = [initial_floor]

    random_steps = random.randint(0, max_random_steps)

    for i in range(random_steps):
        actions = get_possible_moves(current_state)

        if len(actions) == 0:
            break

        action = random.choice(actions)
        next_state = move_vacuum(current_state, action)

        current_state = next_state
        path.append(next_state)

    node = {
        "state": current_state,
        "path": path,
        "cost": count_wrong_cells(current_state)
    }

    return node


# =========================
# LOCAL BEAM SEARCH
# =========================
# Ý tưởng:
# - Không chỉ giữ 1 trạng thái hiện tại như Hill Climbing
# - Thuật toán giữ đồng thời k trạng thái tốt nhất
# - Ban đầu sinh ngẫu nhiên k trạng thái từ Start
# - Ở mỗi vòng lặp:
#   + Sinh tất cả trạng thái lân cận của k trạng thái hiện tại
#   + Nếu gặp Goal thì trả về ngay
#   + Sắp xếp các trạng thái lân cận theo h(n) tăng dần
#   + Chọn k trạng thái tốt nhất làm Current_State_set mới
# - Nếu không còn sinh được trạng thái mới thì trả về None
# =========================
def localbeamsearch(initial_floor, k=2, max_random_steps=10, max_iterations=100):
    current_state_set = []
    used_states = set()

    # Khởi tạo: sinh ngẫu nhiên k trạng thái từ Start
    # attempts dùng để tránh trường hợp sinh trùng quá nhiều trạng thái
    attempts = 0

    while len(current_state_set) < k and attempts < k * 10:
        random_node = random_state_from_start(initial_floor, max_random_steps)
        random_key = state_to_key(random_node["state"])

        if random_key not in used_states:
            current_state_set.append(random_node)
            used_states.add(random_key)

        attempts += 1

    # Nếu không sinh đủ k trạng thái thì thêm Start vào beam
    if len(current_state_set) == 0:
        start_node = {
            "state": initial_floor,
            "path": [initial_floor],
            "cost": count_wrong_cells(initial_floor)
        }

        current_state_set.append(start_node)
        used_states.add(state_to_key(initial_floor))

    for iteration in range(max_iterations):
        neighbor_states = []
        neighbor_keys = set()

        # Kiểm tra đích trong tập trạng thái hiện tại
        for node in current_state_set:
            if goal(node["state"]):
                return node

        # Sinh trạng thái lân cận cho từng State trong Current_State_set
        for node in current_state_set:
            for action in get_possible_moves(node["state"]):
                next_state = move_vacuum(node["state"], action)
                next_key = state_to_key(next_state)

                # Bỏ qua trạng thái đã xét để hạn chế lặp vô hạn
                if next_key in used_states or next_key in neighbor_keys:
                    continue

                next_node = {
                    "state": next_state,
                    "path": node["path"] + [next_state],
                    "cost": count_wrong_cells(next_state)
                }

                neighbor_states.append(next_node)
                neighbor_keys.add(next_key)

        # Kiểm tra đích trong các trạng thái lân cận
        for neighbor in neighbor_states:
            if goal(neighbor["state"]):
                return neighbor

        # Nếu không sinh được trạng thái lân cận mới thì thất bại
        if len(neighbor_states) == 0:
            return None

        # Sắp xếp Neighbor_States theo h(n) tăng dần
        # Vì h(n) là số ô sai nên h càng nhỏ càng tốt
        neighbor_states.sort(key=lambda node: node["cost"])

        # Lấy k trạng thái tốt nhất làm Current_State_set mới
        current_state_set = neighbor_states[:k]

        for node in current_state_set:
            used_states.add(state_to_key(node["state"]))

    # Chạy quá max_iterations mà chưa chạm được goal
    return None
