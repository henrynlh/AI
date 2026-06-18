# =========================
# MAP COLORING BACKTRACKING
# =========================
# Bài toán:
# - Mỗi vùng trên bản đồ là 1 biến
# - Mỗi biến cần được gán 1 màu
# - Hai vùng kề nhau không được có cùng màu
# - Thuật toán dùng Backtracking để thử màu
#   và quay lui khi vi phạm ràng buộc
# =========================


# =========================
# DANH SÁCH VÙNG TRÊN BẢN ĐỒ
# =========================
REGIONS = {
    1: "Củ Chi",
    2: "Hóc Môn",
    3: "Bình Chánh",
    4: "TP. Thủ Đức",
    5: "Quận 12",
    6: "Gò Vấp",
    7: "Tân Bình",
    8: "Bình Thạnh",
    9: "Phú Nhuận",
    10: "Nhà Bè",
    11: "Cần Giờ"
}


# =========================
# MIỀN GIÁ TRỊ
# Sử dụng 4 màu:
# Đỏ, Vàng, Xanh lá, Xanh dương
# =========================
COLORS = ["Đỏ", "Vàng", "Xanh lá", "Xanh dương"]


# =========================
# RÀNG BUỘC KỀ NHAU
# Nếu A kề B thì màu(A) != màu(B)
# =========================
ADJACENCY = {
    1: [2, 3],
    2: [1, 3, 4, 5],
    3: [1, 2, 5, 6],
    4: [2, 5, 8],
    5: [2, 3, 4, 6, 7, 8],
    6: [3, 5, 7, 10],
    7: [5, 6, 8, 9, 10],
    8: [4, 5, 7, 9],
    9: [7, 8, 10, 11],
    10: [6, 7, 9, 11],
    11: [9, 10]
}


# =========================
# THỨ TỰ CHỌN BIẾN
# Chọn theo số thứ tự trên bản đồ
# để quá trình mô phỏng dễ theo dõi
# =========================
REGION_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


# =========================
# KIỂM TRA MÀU CÓ HỢP LỆ KHÔNG
# =========================
# Ý tưởng:
# - Xét vùng region đang cần tô màu
# - Duyệt các vùng kề với region
# - Nếu vùng kề đã được tô cùng màu thì không hợp lệ
# - Nếu không vi phạm ràng buộc thì hợp lệ
# =========================
def is_valid_color(region, color, assignment):
    for neighbor in ADJACENCY[region]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False

    return True


# =========================
# KIỂM TRA ĐÃ TÔ HẾT BẢN ĐỒ CHƯA
# =========================
def is_complete_assignment(assignment):
    return len(assignment) == len(REGION_ORDER)


# =========================
# CHỌN VÙNG CHƯA ĐƯỢC TÔ MÀU
# =========================
def select_unassigned_region(assignment):
    for region in REGION_ORDER:
        if region not in assignment:
            return region

    return None


# =========================
# COPY ASSIGNMENT
# =========================
# Mục đích:
# - Lưu lại trạng thái tại từng bước để UI mô phỏng
# - Tránh việc các bước sau làm thay đổi assignment của bước trước
# =========================
def copy_assignment(assignment):
    copied = {}

    for region in assignment:
        copied[region] = assignment[region]

    return copied


# =========================
# THÊM BƯỚC VÀO DANH SÁCH MÔ PHỎNG
# =========================
def add_step(steps, step_type, region, color, assignment, message):
    step = {
        "type": step_type,
        "region": region,
        "region_name": REGIONS[region] if region is not None else "",
        "color": color,
        "assignment": copy_assignment(assignment),
        "message": message
    }

    steps.append(step)


# =========================
# BACKTRACKING ĐỆ QUY
# =========================
# Ý tưởng:
# - Nếu đã tô hết tất cả vùng thì thành công
# - Chọn 1 vùng chưa tô
# - Thử lần lượt từng màu
# - Nếu màu hợp lệ thì gán màu và gọi đệ quy
# - Nếu nhánh phía sau thất bại thì xóa màu vừa gán và quay lui
# - Nếu không màu nào hợp lệ thì trả về thất bại
# =========================
def backtrack(assignment, steps):
    # Nếu đã tô hết tất cả vùng thì thành công
    if is_complete_assignment(assignment):
        add_step(
            steps,
            "done",
            None,
            None,
            assignment,
            "Hoàn thành: tất cả vùng đã được tô màu hợp lệ."
        )
        return True

    # Chọn vùng chưa tô tiếp theo
    region = select_unassigned_region(assignment)

    add_step(
        steps,
        "select",
        region,
        None,
        assignment,
        f"Chọn vùng tiếp theo: {REGIONS[region]}"
    )

    # Thử lần lượt từng màu trong miền giá trị
    for color in COLORS:
        add_step(
            steps,
            "try",
            region,
            color,
            assignment,
            f"Thử tô {REGIONS[region]} bằng màu {color}."
        )

        # Nếu màu hợp lệ thì gán màu
        if is_valid_color(region, color, assignment):
            assignment[region] = color

            add_step(
                steps,
                "assign",
                region,
                color,
                assignment,
                f"Hợp lệ: gán {REGIONS[region]} = {color}."
            )

            # Gọi đệ quy để tô vùng tiếp theo
            if backtrack(assignment, steps):
                return True

            # Nếu nhánh sau bị kẹt thì quay lui
            old_color = assignment[region]
            del assignment[region]

            add_step(
                steps,
                "backtrack",
                region,
                old_color,
                assignment,
                f"Quay lui: bỏ màu {old_color} khỏi {REGIONS[region]}."
            )

        # Nếu màu không hợp lệ
        else:
            add_step(
                steps,
                "fail",
                region,
                color,
                assignment,
                f"Không hợp lệ: {REGIONS[region]} không thể tô màu {color} vì trùng với vùng kề."
            )

    # Nếu thử hết màu mà không có màu nào dẫn tới lời giải
    return False


# =========================
# HÀM CHÍNH GỌI THUẬT TOÁN
# =========================
def mapcoloringbacktracking():
    assignment = {}
    steps = []

    add_step(
        steps,
        "start",
        None,
        None,
        assignment,
        "Bắt đầu Backtracking với Assignment = {}."
    )

    success = backtrack(assignment, steps)

    if success:
        final_assignment = copy_assignment(assignment)
    else:
        final_assignment = None
        add_step(
            steps,
            "failure",
            None,
            None,
            assignment,
            "Thất bại: không tìm được cách tô màu thỏa mãn ràng buộc."
        )

    result = {
        "success": success,
        "assignment": final_assignment,
        "steps": steps,
        "regions": REGIONS,
        "colors": COLORS,
        "adjacency": ADJACENCY
    }

    return result
