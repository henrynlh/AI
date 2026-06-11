import copy
import heapq
import random

from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum
)


# =========================
# g(n): số ô sai
# Với bài máy hút bụi:
# số ô sai = số ô bẩn còn lại
# Không đếm ô sạch 0
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
# h(n): Manhattan trong 1 trạng thái
# Tính tổng khoảng cách từ V đến các ô bẩn
# Không đếm ô sạch 0
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
# Chuyển state sang dạng có thể lưu trong set
# Mục đích:
# - Tránh xét lại belief_state đã duyệt
# - Dùng làm key cho mỗi trạng thái đơn
# =========================
def state_to_key(state):
    return tuple(tuple(row) for row in state)


# =========================
# Chuyển belief_state sang dạng có thể lưu trong set
# Với Partial Observation Search:
# - 1 belief_state chứa nhiều trạng thái có thể xảy ra
# - Các trạng thái này phải khớp với những ô được nhìn thấy
# =========================
def belief_to_key(belief_state):
    keys = []

    for state in belief_state:
        keys.append(state_to_key(state))

    return tuple(keys)


# =========================
# Chuẩn hóa danh sách ô được nhìn thấy
# Mục đích:
# - UI truyền vào dạng list/set các tuple (i, j)
# - Hàm này đảm bảo dữ liệu luôn đúng dạng tuple
# =========================
def normalize_observed_positions(observed_positions):
    positions = []

    for position in observed_positions:
        i = position[0]
        j = position[1]
        positions.append((i, j))

    return positions


# =========================
# Kiểm tra 1 state có khớp phần nhìn thấy không
# Với Partial Observation Search:
# - Chỉ các ô được Ctrl + Click mới được xem là nhìn thấy
# - State hợp lệ nếu các ô nhìn thấy giống actual_state
# =========================
def match_observation(state, actual_state, observed_positions):
    for i, j in observed_positions:
        if state[i][j] != actual_state[i][j]:
            return False

    return True


# =========================
# Tạo ngẫu nhiên 1 state có thể xảy ra từ các ô được nhìn thấy
# Cách làm:
# - Các ô được nhìn thấy giữ nguyên theo actual_state
# - Các ô chưa nhìn thấy sẽ được random 0 / 1 / vị trí V
# - Mỗi state vẫn chỉ có đúng 1 máy hút bụi V
# =========================
def random_possible_state(actual_state, observed_positions):
    rows = len(actual_state)
    cols = len(actual_state[0])
    observed_set = set(observed_positions)

    fixed_vacuum_position = None
    unobserved_positions = []

    for i in range(rows):
        for j in range(cols):
            if (i, j) in observed_set:
                if actual_state[i][j] == "V":
                    fixed_vacuum_position = (i, j)
            else:
                unobserved_positions.append((i, j))

    # Nếu ô V không nằm trong vùng nhìn thấy
    # thì V có thể nằm ở một ô chưa được nhìn thấy bất kỳ
    if fixed_vacuum_position is None:
        if len(unobserved_positions) > 0:
            vacuum_position = random.choice(unobserved_positions)
        else:
            vacuum_position = find_vacuum_position(actual_state)
    else:
        vacuum_position = fixed_vacuum_position

    state = []

    for i in range(rows):
        row = []

        for j in range(cols):
            if (i, j) in observed_set:
                row.append(actual_state[i][j])
            elif (i, j) == vacuum_position:
                row.append("V")
            else:
                row.append(random.choice([0, 1]))

        state.append(row)

    return state


# =========================
# Tạo belief_state ban đầu cho Partial Observation Search
# Ý nghĩa:
# - Ô phía trên UI là actual_state thật
# - Người dùng Ctrl + Click chọn các ô nhìn thấy
# - Ô phía dưới random 2 trạng thái có thể xảy ra
#   nhưng phải khớp với các ô đã nhìn thấy
# =========================
def create_initial_belief_state(actual_state, observed_positions, state_count=2):
    observed_positions = normalize_observed_positions(observed_positions)

    belief_state = []
    used_keys = set()
    attempts = 0
    max_attempts = state_count * 100

    while len(belief_state) < state_count and attempts < max_attempts:
        state = random_possible_state(actual_state, observed_positions)

        if not match_observation(state, actual_state, observed_positions):
            attempts += 1
            continue

        key = state_to_key(state)

        if key not in used_keys:
            belief_state.append(state)
            used_keys.add(key)

        attempts += 1

    # Nếu random chưa đủ 2 trạng thái thì thêm actual_state làm dự phòng
    # để belief_state luôn có dữ liệu cho thuật toán chạy
    if len(belief_state) == 0:
        belief_state.append(copy.deepcopy(actual_state))

    while len(belief_state) < state_count:
        fallback_state = copy.deepcopy(actual_state)
        key = state_to_key(fallback_state)

        if key not in used_keys:
            belief_state.append(fallback_state)
            used_keys.add(key)
        else:
            # Nếu actual_state đã trùng thì tạo bản khác bằng cách random lại
            state = random_possible_state(actual_state, observed_positions)
            belief_state.append(state)

    return belief_state[:state_count]


# =========================
# Kiểm tra goal cho belief_state
# Với Partial Observation Search:
# - Thuật toán chỉ dừng khi tất cả trạng thái có thể xảy ra đều sạch bụi
# =========================
def belief_goal(belief_state):
    for state in belief_state:
        if not goal(state):
            return False

    return True


# =========================
# g(n) cho belief_state
# g(n) = tổng số ô sai của tất cả trạng thái
# Chỉ đếm ô bẩn 1, không đếm ô sạch 0
# =========================
def count_wrong_cells_in_belief(belief_state):
    wrong = 0

    for state in belief_state:
        wrong += count_wrong_cells(state)

    return wrong


# =========================
# h(n) cho belief_state
# h(n) = tổng Manhattan của tất cả trạng thái
# Chỉ tính khoảng cách đến ô bẩn 1
# Không tính ô sạch 0
# =========================
def manhattan_distance_in_belief(belief_state):
    total_distance = 0

    for state in belief_state:
        total_distance += manhattan_distance(state)

    return total_distance


# =========================
# Lấy tất cả action có thể xuất hiện trong belief_state
# Quy tắc:
# - Ta chọn 1 action chung cho các trạng thái
# - State nào đã goal thì dừng, không sinh action nữa
# =========================
def get_belief_actions(belief_state):
    actions = []

    for state in belief_state:
        if goal(state):
            continue

        for action in get_possible_moves(state):
            if action not in actions:
                actions.append(action)

    return actions


# =========================
# Áp dụng 1 action cho 1 state
# Quy tắc:
# - Nếu state đã goal thì đứng yên
# - Nếu action đi được thì state đó di chuyển
# - Nếu action không đi được thì state đó giữ nguyên
# =========================
def move_state_by_action(state, action):
    if goal(state):
        return copy.deepcopy(state)

    possible_actions = get_possible_moves(state)

    if action in possible_actions:
        return move_vacuum(copy.deepcopy(state), action)

    return copy.deepcopy(state)


# =========================
# Áp dụng 1 action cho toàn bộ belief_state
# Nghĩa là 2 trạng thái cùng nhận một action
# - State nào đi được thì đi
# - State nào không đi được thì giữ nguyên
# - State nào đã xong thì đứng yên chờ state còn lại
# =========================
def move_belief_state(belief_state, action):
    next_belief_state = []

    for state in belief_state:
        next_state = move_state_by_action(state, action)
        next_belief_state.append(next_state)

    return next_belief_state


# =========================
# PARTIAL OBSERVATION SEARCH + A*
# =========================
# Ý tưởng:
# - Môi trường chỉ nhìn thấy một phần
# - Ô phía trên UI là random state thật
# - Người dùng Ctrl + Click chọn các ô được nhìn thấy
# - Ô phía dưới random 2 trạng thái có thể xảy ra
#   từ các ô được nhìn thấy
# - Sau đó thuật toán chạy giống No Observation Search
# - Mỗi node trong A* là 1 belief_state
# - Mỗi bước chọn 1 action chung và áp dụng cho cả 2 trạng thái
# - g(n): tổng số ô sai, chỉ đếm ô bẩn 1, không đếm ô 0
# - h(n): tổng Manhattan đến ô bẩn 1, không đếm ô 0
# - f(n) = g(n) + h(n)
# - State nào goal thì dừng và chờ state còn lại
# - Khi tất cả state trong belief_state đều sạch bụi thì dừng
# =========================
def partialobservationsearch(data):
    actual_state = copy.deepcopy(data["actual_state"])
    observed_positions = normalize_observed_positions(data["observed_positions"])

    if "initial_belief_state" in data and data["initial_belief_state"] is not None:
        initial_belief_state = copy.deepcopy(data["initial_belief_state"])
    else:
        initial_belief_state = create_initial_belief_state(
            actual_state,
            observed_positions,
            state_count=2
        )

    g = count_wrong_cells_in_belief(initial_belief_state)
    h = manhattan_distance_in_belief(initial_belief_state)
    f = g + h

    start_node = {
        "actual_state": actual_state,
        "belief_state": initial_belief_state,
        "state": initial_belief_state,
        "path": [initial_belief_state],
        "actions": [],
        "cost": g,
        "heuristic": h,
        "f": f,
        "observed_positions": observed_positions
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

        # Nếu tất cả state trong belief_state đều sạch thì trả về
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
                "actual_state": actual_state,
                "belief_state": next_belief_state,
                "state": next_belief_state,
                "path": current_node["path"] + [next_belief_state],
                "actions": current_node["actions"] + [action],
                "cost": g,
                "heuristic": h,
                "f": f,
                "observed_positions": observed_positions
            }

            counter += 1

            heapq.heappush(open_list, (
                next_node["f"],
                counter,
                next_node
            ))

    # Nếu open_list rỗng mà chưa tìm thấy goal thì thất bại
    return None
