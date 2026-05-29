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
# SIMPLE HILL CLIMBING
# =========================
# Ý tưởng:
# - Bắt đầu từ trạng thái ban đầu
# - Tính h(n) của trạng thái hiện tại
# - Sinh các trạng thái lân cận
# - Gặp trạng thái đầu tiên có h(n) nhỏ hơn thì đi ngay
# - Nếu không có trạng thái nào tốt hơn thì dừng
# =========================
def simplehillclimbing(initial_floor):
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
        found_better = False

        # Sinh các trạng thái lân cận
        for action in get_possible_moves(current_node["state"]):
            next_state = move_vacuum(current_node["state"], action)
            next_cost = count_wrong_cells(next_state)

            # Vì h(n) là số ô sai nên h càng nhỏ càng tốt
            # Simple Hill Climbing chọn trạng thái đầu tiên tốt hơn
            if next_cost < current_cost:
                current_node = {
                    "state": next_state,
                    "path": current_node["path"] + [next_state],
                    "cost": next_cost
                }

                found_better = True
                break

        # Nếu không có trạng thái lân cận nào tốt hơn
        # và hiện tại chưa phải goal thì xem như không tìm thấy lời giải
        if not found_better:
            return None