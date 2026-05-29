from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum,
    state_key,
    find_vacuum
)


# =========================
# g(n): số ô sai
# Với bài máy hút bụi: số ô bẩn còn lại
# =========================
def count_wrong_cells(state):
    wrong = 0

    for row in state:
        for cell in row:
            if cell == 1:
                wrong += 1

    return wrong


# =========================
# Tính khoảng cách Manhattan
# =========================
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# =========================
# h(n): khoảng cách Manhattan
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

    # Nếu không còn ô bẩn thì h(n) = 0
    if min_distance is None:
        return 0

    return min_distance


# =========================
# Tính f(n) = g(n) + h(n)
# =========================
def calculate_f(g, h):
    return g + h


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
# Kiểm tra state đã nằm trong path chưa
# Dùng để tránh lặp vòng
# =========================
def in_path(state, path):
    key = state_key(state)

    for old_state in path:
        if state_key(old_state) == key:
            return True

    return False


# =========================
# Tạo node
# =========================
def create_node(state, path):
    g = count_wrong_cells(state)
    h = manhattan_cost(state)
    f = calculate_f(g, h)

    node = {
        "state": state,
        "path": path,
        "g": g,
        "h": h,
        "cost": f
    }

    return node


# =========================
# TÌM KIẾM TRONG 1 GIỚI HẠN BOUND
# =========================
# Nếu f(n) <= bound:
#     thêm node vào frontier
#
# Nếu f(n) > bound:
#     cắt node đó
#     lưu lại g(n) để tăng bound
#
# Trong frontier:
#     chọn node có cost nhỏ nhất để xét trước
# =========================
def bounded_search(initial_floor, bound):
    start_node = create_node(initial_floor, [initial_floor])

    frontier = []
    reached = dict()

    min_g_cut = None

    # Kiểm tra Start trước
    if start_node["cost"] <= bound:
        frontier.append(start_node)
        reached[state_key(initial_floor)] = start_node["cost"]
    else:
        min_g_cut = start_node["g"]
        return None, min_g_cut

    while len(frontier) > 0:
        # Chọn node có cost nhỏ nhất giống A*
        node = pop_min_cost(frontier)

        # Nếu là goal thì trả về kết quả
        if goal(node["state"]):
            return node, None

        for action in get_possible_moves(node["state"]):
            child_state = move_vacuum(node["state"], action)
            child_key = state_key(child_state)

            # Tránh quay lại trạng thái đã nằm trong đường đi hiện tại
            if in_path(child_state, node["path"]):
                continue

            child = create_node(
                child_state,
                node["path"] + [child_state]
            )

            # Nếu f(con) <= bound thì cho vào frontier
            if child["cost"] <= bound:
                if child_key not in reached or child["cost"] < reached[child_key]:
                    reached[child_key] = child["cost"]
                    frontier.append(child)

            # Nếu f(con) > bound thì cắt và lưu min(g)
            else:
                if min_g_cut is None or child["g"] < min_g_cut:
                    min_g_cut = child["g"]

    return None, min_g_cut


# =========================
# IDA*
# =========================
# g(n) = số ô sai / số ô bẩn còn lại
# h(n) = khoảng cách Manhattan tới ô bẩn gần nhất
# f(n) = g(n) + h(n)
#
# bound ban đầu = g(Start)
#
# Nếu f(n) <= bound:
#     cho node vào frontier
#
# Nếu f(n) > bound:
#     cắt node đó
#
# Trong frontier:
#     chọn node có cost nhỏ nhất để xét trước
#
# Nếu chưa tìm được goal:
#     bound = bound + min(g(n)) của các node bị cắt
# =========================
def idastar(initial_floor):
    start_g = count_wrong_cells(initial_floor)

    # Nếu trạng thái ban đầu đã là goal
    if goal(initial_floor):
        return create_node(initial_floor, [initial_floor])

    # Giới hạn ban đầu = g(Start)
    bound = start_g

    while True:
        result, min_g_cut = bounded_search(initial_floor, bound)

        # Nếu tìm thấy lời giải
        if result is not None:
            return result

        # Nếu không còn node nào bị cắt để tăng bound
        if min_g_cut is None:
            return None

        # Tránh trường hợp bound không tăng
        if min_g_cut == 0:
            min_g_cut = 1

        # Tăng bound theo min(g(n)) của các node bị cắt
        bound = bound + min_g_cut