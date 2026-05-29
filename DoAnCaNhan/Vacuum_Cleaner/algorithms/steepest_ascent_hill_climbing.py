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
# STEEPEST ASCENT HILL CLIMBING
# =========================
# Ý tưởng:
# - Bắt đầu từ trạng thái ban đầu
# - Sinh TẤT CẢ trạng thái lân cận
# - Chọn trạng thái lân cận tốt nhất
# - Nếu trạng thái tốt nhất tốt hơn trạng thái hiện tại thì đi tiếp
# - Nếu không có trạng thái nào tốt hơn thì dừng
# =========================
def steepestascenthillclimbing(initial_floor):
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

        best_neighbor = None
        best_cost = current_cost

        # Sinh tất cả trạng thái lân cận
        for action in get_possible_moves(current_node["state"]):
            next_state = move_vacuum(current_node["state"], action)
            next_cost = count_wrong_cells(next_state)

            # Vì h(n) là số ô sai nên h càng nhỏ càng tốt
            # Chọn trạng thái lân cận có h(n) nhỏ nhất
            if next_cost < best_cost:
                best_neighbor = next_state
                best_cost = next_cost

        # Nếu tìm được trạng thái tốt hơn thì cập nhật current
        if best_neighbor is not None:
            current_node = {
                "state": best_neighbor,
                "path": current_node["path"] + [best_neighbor],
                "cost": best_cost
            }

        # Nếu không có trạng thái lân cận nào tốt hơn
        # và hiện tại chưa phải goal thì xem như không tìm thấy lời giải
        else:
            return None