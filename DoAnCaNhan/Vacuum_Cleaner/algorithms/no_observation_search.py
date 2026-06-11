import copy
import heapq
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
# Lưu ý: chỉ đếm ô 1, không đếm ô 0
# =========================
def count_wrong_cells(state):
    wrong = 0

    for row in state:
        for cell in row:
            if cell == 1:
                wrong += 1

    return wrong


# =========================
# Tìm vị trí máy hút bụi V
# =========================
def find_vacuum_position(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == "V":
                return i, j

    return None


# =========================
# Manhattan cho 1 state
# Với bài máy hút bụi:
# - Chỉ tính khoảng cách từ V đến các ô bẩn 1
# - Không tính các ô sạch 0
# =========================
def manhattan_distance(state):
    vacuum_position = find_vacuum_position(state)

    if vacuum_position is None:
        return 0

    vacuum_i, vacuum_j = vacuum_position
    total_distance = 0

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 1:
                total_distance += abs(vacuum_i - i) + abs(vacuum_j - j)

    return total_distance


# =========================
# Kiểm tra dữ liệu có phải belief_state không
# state thường: [[...], [...]]
# belief_state: [state_1, state_2]
# =========================
def is_belief_state(data):
    if not isinstance(data, list):
        return False

    if len(data) == 0:
        return False

    if not isinstance(data[0], list):
        return False

    if len(data[0]) == 0:
        return False

    if not isinstance(data[0][0], list):
        return False

    return True


# =========================
# Chuyển state sang dạng có thể lưu trong set
# Mục đích:
# - Tránh xét lại belief_state đã duyệt
# - Dùng làm key cho mỗi trạng thái đơn
# =========================
def state_to_key(state):
    return tuple(tuple(row) for row in state)


# =========================
# Chuyển belief_state sang dạng có thể lưu trong set
# Với No Observation Search:
# - 1 belief_state chứa nhiều trạng thái có thể xảy ra
# - Ở đây dùng 2 trạng thái ban đầu
# =========================
def belief_to_key(belief_state):
    keys = []

    for state in belief_state:
        keys.append(state_to_key(state))

    return tuple(keys)


# =========================
# Sinh ngẫu nhiên 1 trạng thái từ Start
# Cách làm:
# - Bắt đầu từ initial_floor
# - Đi ngẫu nhiên một số bước
# - Trạng thái nhận được xem như 1 trạng thái có thể xảy ra
# =========================
def random_state_from_start(initial_floor, max_random_steps=10):
    current_state = copy.deepcopy(initial_floor)

    random_steps = random.randint(1, max_random_steps)

    for i in range(random_steps):
        actions = get_possible_moves(current_state)

        if len(actions) == 0:
            break

        action = random.choice(actions)
        current_state = move_vacuum(current_state, action)

    return current_state


# =========================
# Tạo trạng thái thứ 2 từ Start
# Cách làm:
# - Sinh ngẫu nhiên 1 trạng thái từ Start
# - Nếu bị trùng với Start thì đổi nhẹ 1 ô sạch 0 thành ô bẩn 1
# =========================
def create_second_initial_state(initial_floor):
    second_state = random_state_from_start(initial_floor)

    if state_to_key(second_state) != state_to_key(initial_floor):
        return second_state

    second_state = copy.deepcopy(initial_floor)

    for i in range(len(second_state)):
        for j in range(len(second_state[i])):
            if second_state[i][j] == 0:
                second_state[i][j] = 1
                return second_state

    return second_state


# =========================
# Tự khởi tạo belief_state ban đầu gồm 2 trạng thái
# Ý nghĩa:
# - Không quan sát được nên không chắc trạng thái thật là trạng thái nào
# - Ta lưu đồng thời 2 trạng thái có thể xảy ra
# - Nếu UI đã truyền sẵn belief_state thì giữ nguyên belief_state đó
# =========================
def create_initial_belief_state(initial_floor):
    if is_belief_state(initial_floor):
        return copy.deepcopy(initial_floor)

    state_1 = copy.deepcopy(initial_floor)
    state_2 = create_second_initial_state(initial_floor)

    belief_state = [state_1, state_2]

    return belief_state


# =========================
# Kiểm tra goal cho belief_state
# Với No Observation Search:
# - Thuật toán chỉ dừng khi tất cả trạng thái có thể xảy ra đều sạch bụi
# =========================
def belief_goal(belief_state):
    for state in belief_state:
        if not goal(state):
            return False

    return True


# =========================
# g(n) cho belief_state
# Theo yêu cầu bài toán:
# - g(n) = tổng số ô sai của các trạng thái trong belief_state
# - Chỉ đếm ô bẩn 1, không đếm ô sạch 0
# =========================
def count_wrong_cells_in_belief(belief_state):
    wrong = 0

    for state in belief_state:
        wrong += count_wrong_cells(state)

    return wrong


# =========================
# h(n) cho belief_state
# Theo yêu cầu bài toán:
# - h(n) = tổng Manhattan của các trạng thái trong belief_state
# - Chỉ tính khoảng cách đến ô bẩn 1
# - Không tính ô sạch 0
# =========================
def manhattan_distance_in_belief(belief_state):
    total_distance = 0

    for state in belief_state:
        total_distance += manhattan_distance(state)

    return total_distance


# =========================
# Lấy tất cả action có thể xuất hiện trong belief_state
# Với No Observation Search:
# - Ta chọn 1 action chung
# - Action đó sẽ được áp dụng đồng thời cho các trạng thái chưa xong
# - Trạng thái nào đã goal thì không cần sinh action nữa
# =========================
def get_belief_actions(belief_state):
    actions = []

    for state in belief_state:
        # Nếu state này đã sạch hết bụi thì state này dừng lại
        # và chờ các state khác tiếp tục tìm đường
        if goal(state):
            continue

        for action in get_possible_moves(state):
            if action not in actions:
                actions.append(action)

    return actions


# =========================
# Áp dụng 1 action cho 1 state
# Quy tắc:
# - Nếu state đã goal thì giữ nguyên, không cho di chuyển nữa
# - Nếu action đi được thì state đó di chuyển
# - Nếu action không đi được thì state đó giữ nguyên
# Ví dụ:
# - Cùng action là đi trái
# - State 1 đi trái được thì đi
# - State 2 đi trái không được thì đứng yên
# =========================
def move_state_by_action(state, action):
    # Trạng thái nào đã sạch hết bụi thì dừng luôn
    # Không di chuyển tiếp để tránh làm sai kết quả đã đạt được
    if goal(state):
        return copy.deepcopy(state)

    possible_actions = get_possible_moves(state)

    if action in possible_actions:
        return move_vacuum(copy.deepcopy(state), action)

    return copy.deepcopy(state)


# =========================
# Áp dụng 1 action cho toàn bộ belief_state
# Nghĩa là 2 trạng thái cùng nhận 1 action chung
# Nhưng mỗi trạng thái xử lý theo khả năng riêng:
# - Đi được thì đi
# - Không đi được thì giữ nguyên
# - Đã goal thì dừng và chờ trạng thái còn lại
# =========================
def move_belief_state(belief_state, action):
    next_belief_state = []

    for state in belief_state:
        next_state = move_state_by_action(state, action)
        next_belief_state.append(next_state)

    return next_belief_state


# =========================
# NO OBSERVATION SEARCH + A*
# =========================
# Ý tưởng:
# - Không quan sát được chính xác trạng thái thật
# - Tự khởi tạo 2 trạng thái ban đầu tạo thành belief_state
# - Mỗi node trong A* là 1 belief_state
# - Mỗi bước chọn 1 action chung và áp dụng cho cả 2 trạng thái
# - Trạng thái nào đã goal thì dừng lại, chờ trạng thái còn lại
# - g(n): số ô sai, chỉ đếm ô bẩn 1, không đếm ô 0
# - h(n): tổng Manhattan đến các ô bẩn, không đếm ô 0
# - f(n) = g(n) + h(n)
# - Khi tất cả trạng thái trong belief_state đều sạch bụi thì dừng toàn bộ thuật toán
# =========================
def noobservationastar(initial_floor):
    initial_belief_state = create_initial_belief_state(initial_floor)

    start_g = count_wrong_cells_in_belief(initial_belief_state)
    start_h = manhattan_distance_in_belief(initial_belief_state)
    start_f = start_g + start_h

    start_node = {
        "belief_state": initial_belief_state,
        "state": initial_belief_state,
        "path": [initial_belief_state],
        "actions": [],
        "cost": start_g,
        "heuristic": start_h,
        "f": start_f
    }

    open_list = []
    closed_list = set()

    counter = 0

    heapq.heappush(open_list, (
        start_node["f"],
        counter,
        start_node
    ))

    while len(open_list) > 0:
        # Lấy node có f nhỏ nhất ra khỏi open_list
        current_item = heapq.heappop(open_list)
        current_node = current_item[2]

        current_belief_state = current_node["belief_state"]
        current_key = belief_to_key(current_belief_state)

        # Nếu belief_state này đã xét rồi thì bỏ qua
        if current_key in closed_list:
            continue

        closed_list.add(current_key)

        # Nếu tất cả trạng thái trong belief_state đều sạch thì trả về
        if belief_goal(current_belief_state):
            return current_node

        actions = get_belief_actions(current_belief_state)

        # Nếu không còn action nào thì bỏ qua node này
        if len(actions) == 0:
            continue

        # Sinh các belief_state lân cận
        for action in actions:
            next_belief_state = move_belief_state(current_belief_state, action)
            next_key = belief_to_key(next_belief_state)

            if next_key in closed_list:
                continue

            g = count_wrong_cells_in_belief(next_belief_state)
            h = manhattan_distance_in_belief(next_belief_state)
            f = g + h

            next_node = {
                "belief_state": next_belief_state,
                "state": next_belief_state,
                "path": current_node["path"] + [next_belief_state],
                "actions": current_node["actions"] + [action],
                "cost": g,
                "heuristic": h,
                "f": f
            }

            counter += 1

            heapq.heappush(open_list, (
                next_node["f"],
                counter,
                next_node
            ))

    # Nếu open_list rỗng mà chưa tìm thấy goal thì thất bại
    return None
