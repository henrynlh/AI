# =========================
# AC-3 MAP COLORING CSP - BALANCED LOG
# =========================
# - Thuật toán vẫn xử lý đầy đủ các arc trong Q.
# - Log không hiển thị từng arc không thay đổi domain để tránh quá dài.
#   + Chọn vùng
#   + Thử màu
#   + Gán màu
#   + AC-3 bắt đầu
#   + Domain bị rút gọn
#   + Cập nhật Q
#   + AC-3 kết thúc
#   + Quay lui / hoàn thành
# =========================


# =========================
# DANH SÁCH VÙNG
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
# KÝ HIỆU NGẮN
# =========================
REGION_CODES = {
    1: "CC",
    2: "HM",
    3: "BC",
    4: "TD",
    5: "Q12",
    6: "GV",
    7: "TB",
    8: "BTh",
    9: "PN",
    10: "NB",
    11: "CG"
}


# =========================
# MIỀN GIÁ TRỊ
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


REGION_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


# =========================
# HÀM TIỆN ÍCH
# =========================
def create_initial_domains():
    domains = {}

    for region in REGION_ORDER:
        domains[region] = COLORS.copy()

    return domains


def create_all_arcs():
    queue = []

    for region in REGION_ORDER:
        for neighbor in ADJACENCY[region]:
            queue.append((region, neighbor))

    return queue


def copy_assignment(assignment):
    copied = {}

    for region in assignment:
        copied[region] = assignment[region]

    return copied


def copy_domains(domains):
    copied = {}

    for region in domains:
        copied[region] = domains[region].copy()

    return copied


def format_domain(region, domains):
    return "D(" + REGION_CODES[region] + ")={" + ", ".join(domains[region]) + "}"


def format_arc(arc):
    xi, xj = arc
    return REGION_CODES[xi] + "-" + REGION_CODES[xj]


def format_removed_values(removed_values):
    if len(removed_values) == 0:
        return "Không xóa màu"

    texts = []

    for region, color in removed_values:
        texts.append(color + " khỏi D(" + REGION_CODES[region] + ")")

    return "Xóa " + "; ".join(texts)


def format_added_arcs(added_arcs):
    if len(added_arcs) == 0:
        return "{}"

    texts = []

    for arc in added_arcs:
        texts.append(format_arc(arc))

    return "{ " + ", ".join(texts) + " }"


def is_valid_color(region, color, assignment):
    for neighbor in ADJACENCY[region]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False

    return True


def is_complete_assignment(assignment):
    return len(assignment) == len(REGION_ORDER)


def select_unassigned_region(assignment, domains):
    # MRV đơn giản: chọn vùng chưa tô có domain nhỏ nhất.
    unassigned_regions = []

    for region in REGION_ORDER:
        if region not in assignment:
            unassigned_regions.append(region)

    if len(unassigned_regions) == 0:
        return None

    best_region = unassigned_regions[0]

    for region in unassigned_regions:
        if len(domains[region]) < len(domains[best_region]):
            best_region = region

    return best_region


# =========================
# THÊM STEP CHO UI
# =========================
def add_step(
    steps,
    step_type,
    region,
    color,
    assignment,
    domains,
    message,
    removed_values=None,
    arc=None,
    queue=None,
    manual_log=None
):
    if removed_values is None:
        removed_values = []

    if queue is None:
        queue_snapshot = []
    else:
        queue_snapshot = queue.copy()

    if manual_log is None:
        manual_log = []

    steps.append({
        "type": step_type,
        "region": region,
        "region_name": REGIONS[region] if region is not None else "",
        "color": color,
        "assignment": copy_assignment(assignment),
        "domains": copy_domains(domains),
        "removed_values": removed_values.copy(),
        "arc": arc,
        "queue": queue_snapshot,
        "manual_log": manual_log.copy(),
        "message": message
    })


# =========================
# AC-3 CORE
# =========================
def constraint_satisfied(color_i, color_j):
    return color_i != color_j


def rm_inconsistent_values(domains, xi, xj):
    removed = False
    removed_values = []

    for color_i in domains[xi].copy():
        has_support = False

        for color_j in domains[xj]:
            if constraint_satisfied(color_i, color_j):
                has_support = True
                break

        if not has_support:
            domains[xi].remove(color_i)
            removed_values.append((xi, color_i))
            removed = True

    return removed, removed_values


def add_arc_if_absent(queue, arc):
    # Giữ Q gọn như tập hợp khi mô phỏng.
    if arc not in queue:
        queue.append(arc)
        return True

    return False


def ac3(domains, steps, assignment):
    queue = create_all_arcs()
    checked_count = 0
    revised_count = 0

    add_step(
        steps,
        "ac3_start",
        None,
        None,
        assignment,
        domains,
        "Chạy AC-3.",
        queue=queue,
        manual_log=[
            "Q = tất cả các arc của CSP",
            "Số arc ban đầu: " + str(len(queue))
        ]
    )

    while len(queue) > 0:
        current_arc = queue.pop(0)
        checked_count += 1
        xi, xj = current_arc

        removed, removed_values = rm_inconsistent_values(domains, xi, xj)

        # Vẫn xét arc, nhưng nếu không làm đổi domain thì không ghi log.
        if not removed:
            continue

        revised_count += 1

        add_step(
            steps,
            "ac3_revise",
            xi,
            None,
            assignment,
            domains,
            "AC-3 rút gọn domain.",
            removed_values=removed_values,
            arc=current_arc,
            queue=queue,
            manual_log=[
                "Arc: " + format_arc(current_arc),
                format_removed_values(removed_values),
                "Domain mới: " + format_domain(xi, domains)
            ]
        )

        if len(domains[xi]) == 0:
            add_step(
                steps,
                "domain_empty",
                xi,
                None,
                assignment,
                domains,
                "Domain rỗng.",
                arc=current_arc,
                queue=queue,
                manual_log=[
                    format_domain(xi, domains),
                    "Kết luận: nhánh này thất bại."
                ]
            )
            return False

        added_arcs = []

        # Nếu D(Xi) thay đổi thì thêm (Xk, Xi) với mọi Xk thuộc NEIGHBORS[Xi].
        for xk in ADJACENCY[xi]:
            new_arc = (xk, xi)

            if add_arc_if_absent(queue, new_arc):
                added_arcs.append(new_arc)

        add_step(
            steps,
            "ac3_add_arcs",
            xi,
            None,
            assignment,
            domains,
            "Cập nhật Q.",
            arc=current_arc,
            queue=queue,
            manual_log=[
                "Vì D(" + REGION_CODES[xi] + ") thay đổi",
                "Thêm vào Q: " + format_added_arcs(added_arcs),
                "Q còn: " + str(len(queue)) + " arc"
            ]
        )

    add_step(
        steps,
        "ac3_done",
        None,
        None,
        assignment,
        domains,
        "AC-3 hoàn tất.",
        queue=queue,
        manual_log=[
            "Đã xét: " + str(checked_count) + " arc",
            "Số lần domain bị rút gọn: " + str(revised_count)
        ]
    )

    return True


# =========================
# BACKTRACKING + AC-3
# =========================
def backtracking_ac3(assignment, domains, steps):
    if is_complete_assignment(assignment):
        add_step(
            steps,
            "done",
            None,
            None,
            assignment,
            domains,
            "Hoàn thành tô màu bản đồ.",
            manual_log=[
                "Tất cả vùng đã được tô.",
                "Không có hai vùng kề nhau trùng màu."
            ]
        )
        return True

    region = select_unassigned_region(assignment, domains)

    add_step(
        steps,
        "select",
        region,
        None,
        assignment,
        domains,
        "Chọn vùng chưa tô.",
        manual_log=[
            "Chọn: " + REGIONS[region] + " (" + REGION_CODES[region] + ")",
            format_domain(region, domains)
        ]
    )

    for color in domains[region].copy():
        add_step(
            steps,
            "try",
            region,
            color,
            assignment,
            domains,
            "Thử màu.",
            manual_log=[
                REGION_CODES[region] + " = " + color
            ]
        )

        if not is_valid_color(region, color, assignment):
            add_step(
                steps,
                "fail",
                region,
                color,
                assignment,
                domains,
                "Màu không hợp lệ.",
                manual_log=[
                    "Loại " + color + " vì trùng với vùng kề đã tô."
                ]
            )
            continue

        new_assignment = copy_assignment(assignment)
        new_domains = copy_domains(domains)

        new_assignment[region] = color
        new_domains[region] = [color]

        add_step(
            steps,
            "assign",
            region,
            color,
            new_assignment,
            new_domains,
            "Gán màu.",
            manual_log=[
                "Gán: " + REGION_CODES[region] + " = " + color,
                "Rút gọn: " + format_domain(region, new_domains)
            ]
        )

        ac3_success = ac3(new_domains, steps, new_assignment)

        if ac3_success:
            if backtracking_ac3(new_assignment, new_domains, steps):
                assignment.clear()

                for key in new_assignment:
                    assignment[key] = new_assignment[key]

                return True

        else:
            add_step(
                steps,
                "backtrack",
                region,
                color,
                assignment,
                domains,
                "Quay lui.",
                manual_log=[
                    "AC-3 phát hiện domain rỗng.",
                    "Bỏ nhánh " + REGION_CODES[region] + " = " + color
                ]
            )
            continue

        add_step(
            steps,
            "backtrack",
            region,
            color,
            assignment,
            domains,
            "Quay lui.",
            manual_log=[
                "Nhánh " + REGION_CODES[region] + " = " + color + " không dẫn tới lời giải."
            ]
        )

    return False


# =========================
# HÀM CHÍNH
# =========================
def ac3search():
    assignment = {}
    domains = create_initial_domains()
    steps = []

    add_step(
        steps,
        "start",
        None,
        None,
        assignment,
        domains,
        "Bắt đầu AC-3 kết hợp Backtracking.",
        manual_log=[
            "Mục tiêu: tô màu bản đồ.",
            "AC-3 dùng để rút gọn domain sau mỗi lần gán màu."
        ]
    )

    success = backtracking_ac3(assignment, domains, steps)

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
            domains,
            "Không tìm được lời giải.",
            manual_log=[
                "Không còn nhánh hợp lệ."
            ]
        )

    return {
        "success": success,
        "assignment": final_assignment,
        "steps": steps,
        "regions": REGIONS,
        "colors": COLORS,
        "adjacency": ADJACENCY,
        "domains": domains
    }
