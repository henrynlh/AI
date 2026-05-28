from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum,
    state_key
)


# =========================
# Đếm số ô bẩn
# =========================
def count_dirty_cells(state):
    dirty = 0

    for row in state:
        for cell in row:
            if cell == 1:
                dirty += 1

    return dirty


# =========================
# Tính f(n) = g(n) + h(n)
# =========================
def calculate_f(g, h):
    return g + h


# =========================
# Lấy node có cost nhỏ nhất trong frontier
# cost ở đây chính là f(n)
# =========================
def pop_min_cost(frontier):
    min_index = 0

    for i in range(1, len(frontier)):
        if frontier[i]["cost"] < frontier[min_index]["cost"]:
            min_index = i

    return frontier.pop(min_index)


# =========================
# A* SEARCH
# f(n) = g(n) + h(n)
# g(n) = chi phí cộng dồn từ Start đến node hiện tại
# h(n) = số ô bẩn còn lại
# cost = f(n)
# =========================
def astar(initial_floor):
    # Trạng thái ban đầu
    h_start = count_dirty_cells(initial_floor)
    g_start = 0
    f_start = calculate_f(g_start, h_start)

    node = {
        "state": initial_floor,
        "path": [initial_floor],
        "g": g_start,
        "h": h_start,
        "cost": f_start
    }

    frontier = []
    frontier.append(node)

    # Lưu g nhỏ nhất đã biết của mỗi trạng thái
    reached = dict()
    reached[state_key(initial_floor)] = g_start

    while len(frontier) > 0:
        # A*: lấy node có f(n) nhỏ nhất
        node = pop_min_cost(frontier)

        key = state_key(node["state"])

        # Nếu đã có đường đi tốt hơn tới state này thì bỏ qua
        if node["g"] > reached[key]:
            continue

        # Kiểm tra goal sau khi lấy node ra khỏi frontier
        if goal(node["state"]):
            return node

        for action in get_possible_moves(node["state"]):
            child_state = move_vacuum(node["state"], action)
            child_key = state_key(child_state)

            # cost bước đi = số ô bẩn của trạng thái con
            step_cost = count_dirty_cells(child_state)

            # g(con) = g(cha) + cost bước đi
            child_g = node["g"] + step_cost

            # h(con) = số ô bẩn còn lại của trạng thái con
            child_h = count_dirty_cells(child_state)

            # f(con) = g(con) + h(con)
            child_f = calculate_f(child_g, child_h)

            child = {
                "state": child_state,
                "path": node["path"] + [child_state],
                "g": child_g,
                "h": child_h,
                "cost": child_f
            }

            # Nếu state chưa gặp hoặc có g tốt hơn thì thêm vào frontier
            if child_key not in reached or child_g < reached[child_key]:
                reached[child_key] = child_g
                frontier.append(child)

    return None