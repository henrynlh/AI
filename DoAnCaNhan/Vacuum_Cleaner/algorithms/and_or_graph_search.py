import copy

from core.vacuum_problem import (
    goal,
    get_possible_moves,
    move_vacuum
)


# =========================
# h(n): số ô sai
# Với bài máy hút bụi:
# số ô sai = số ô bẩn còn lại
# Hàm này chỉ dùng để lưu cost hiển thị trên UI
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
# - Tránh lặp lại trạng thái trong nhánh hiện tại
# - Ví dụ tránh vòng lặp A -> B -> A -> B ...
# =========================
def state_to_key(state):
    return tuple(tuple(row) for row in state)


# =========================
# Sinh các trạng thái kết quả sau 1 hành động
# Với bài máy hút bụi:
# - Môi trường đang xét là xác định
# - 1 hành động chỉ sinh ra 1 trạng thái kế tiếp
#
# Tuy nhiên vẫn trả về list để đúng cấu trúc AND-OR Search:
# - OR node chọn action
# - AND node kiểm tra tất cả outcome của action đó
# =========================
def get_action_results(state, action):
    results = []

    next_state = move_vacuum(copy.deepcopy(state), action)
    results.append(next_state)

    return results


# =========================
# OR SEARCH
# =========================
# Ý tưởng:
# - OR node là nơi thuật toán được quyền chọn 1 hành động
# - Nếu trạng thái hiện tại là goal thì thành công
# - Nếu trạng thái đã nằm trong path hiện tại thì thất bại
# - Nếu chưa goal thì thử lần lượt các action có thể đi
# - Action nào dẫn tới lời giải thì chọn action đó
# - Nếu tất cả action đều thất bại thì OR node thất bại
# =========================
def or_search(state, path_keys, depth, max_depth):
    # Nếu vượt quá độ sâu tối đa thì xem như thất bại
    # Mục đích: tránh đệ quy quá sâu hoặc lặp vô hạn
    if depth > max_depth:
        return None

    # Nếu trạng thái hiện tại là goal
    # thì không cần thực hiện thêm hành động nào nữa
    if goal(state):
        return []

    state_key = state_to_key(state)

    # Nếu trạng thái này đã xuất hiện trong nhánh hiện tại
    # thì nhánh này bị lặp, xem như thất bại
    if state_key in path_keys:
        return None

    # Lưu trạng thái hiện tại vào path của nhánh đang xét
    new_path_keys = path_keys.copy()
    new_path_keys.add(state_key)

    # Sinh các action có thể thực hiện từ trạng thái hiện tại
    actions = get_possible_moves(state)

    # Nếu không còn action nào để đi
    # mà trạng thái hiện tại chưa phải goal thì thất bại
    if len(actions) == 0:
        return None

    # OR node: thử từng action
    # Có nhiều đường thì thuật toán lấy đường đầu tiên tìm được
    # theo thứ tự action do get_possible_moves trả về
    for action in actions:
        # Sau khi chọn action, action có thể sinh ra nhiều kết quả
        # Các kết quả đó sẽ được kiểm tra ở AND node
        result_states = get_action_results(state, action)

        result = and_search(
            result_states,
            new_path_keys,
            depth + 1,
            max_depth
        )

        # Nếu AND node thành công
        # nghĩa là action này dẫn tới lời giải
        if result is not None:
            plan = []

            # Lưu các trạng thái sinh ra sau action vào đường đi
            for result_state in result_states:
                plan.append(copy.deepcopy(result_state))

            # Nối tiếp phần đường đi phía sau
            plan.extend(result)

            return plan

    # Nếu tất cả action đều thất bại
    # thì OR node thất bại
    return None


# =========================
# AND SEARCH
# =========================
# Ý tưởng:
# - AND node kiểm tra tất cả trạng thái kết quả sau 1 action
# - Nếu có 1 trạng thái con không tìm được đường tới goal
#   thì toàn bộ action đó thất bại
# - Nếu tất cả trạng thái con đều giải được
#   thì AND node thành công
# =========================
def and_search(states, path_keys, depth, max_depth):
    # Nếu không có trạng thái con nào
    # thì xem như thành công
    if len(states) == 0:
        return []

    all_results = []

    # AND node: tất cả state con đều phải thành công
    for state in states:
        result = or_search(
            state,
            path_keys,
            depth,
            max_depth
        )

        # Chỉ cần 1 state con thất bại
        # thì toàn bộ AND node thất bại
        if result is None:
            return None

        all_results.extend(result)

    return all_results


# =========================
# AND-OR SEARCH
# =========================
# Ý tưởng:
# - Bắt đầu từ 1 trạng thái ban đầu giống các thuật toán khác
# - Trạng thái ban đầu được xem là OR node
# - OR node chọn 1 action để thử
# - Sau mỗi action, AND node kiểm tra các trạng thái kết quả
# - Nếu action nào dẫn tới goal thì trả về đường đi
# - Nếu tất cả action đều thất bại thì trả về None
#
# Lưu ý:
# - Nếu có nhiều lời giải, thuật toán trả về lời giải đầu tiên tìm được
# =========================
def andorgraphsearch(initial_floor, max_depth=80):
    start_state = copy.deepcopy(initial_floor)

    result = or_search(
        start_state,
        set(),
        0,
        max_depth
    )

    # Nếu không tìm được đường tới goal
    if result is None:
        return None

    path = [start_state] + result
    final_state = path[-1]

    node = {
        "state": final_state,
        "path": path,
        "cost": count_wrong_cells(final_state)
    }

    return node
