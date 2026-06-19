# =========================
# MIN-CONFLICTS MAP COLORING CSP - RANDOM INITIAL STATE
# =========================
# - Trạng thái ban đầu là assignment hoàn chỉnh NGẪU NHIÊN.
# - Mỗi lần bấm Solve có thể ra trạng thái ban đầu khác nhau.
# - Log:
#   + current ban đầu
#   + xung đột hiện tại
#   + biến xung đột được chọn
#   + điểm xung đột của từng màu
#   + màu được cập nhật
# =========================

import random


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
def create_domains():
    domains = {}

    for region in REGION_ORDER:
        domains[region] = COLORS.copy()

    return domains


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


def format_assignment_short(assignment):
    parts = []

    for region in REGION_ORDER:
        if region in assignment:
            parts.append(REGION_CODES[region] + "=" + assignment[region])

    return "{ " + ", ".join(parts) + " }"


def format_conflicts(conflicts):
    if len(conflicts) == 0:
        return "Không còn xung đột"

    parts = []

    for a, b in conflicts:
        parts.append(REGION_CODES[a] + "-" + REGION_CODES[b])

    return ", ".join(parts)


def format_scores(scores):
    parts = []

    for color in COLORS:
        parts.append(color + "=" + str(scores[color]))

    return "{ " + ", ".join(parts) + " }"


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
    manual_log=None,
    scores=None,
    conflicts=None
):
    if manual_log is None:
        manual_log = []

    if scores is None:
        scores = {}

    if conflicts is None:
        conflicts = []

    steps.append({
        "type": step_type,
        "region": region,
        "region_name": REGIONS[region] if region is not None else "",
        "color": color,
        "assignment": copy_assignment(assignment),
        "domains": copy_domains(domains),
        "removed_values": [],
        "arc": None,
        "queue": [],
        "manual_log": manual_log.copy(),
        "scores": scores.copy(),
        "conflicts": conflicts.copy(),
        "message": message
    })


# =========================
# KHỞI TẠO ASSIGNMENT HOÀN CHỈNH NGẪU NHIÊN
# =========================
# current <- an initial complete assignment for csp
# Assignment ban đầu có đủ tất cả biến, nhưng có thể còn xung đột.
# =========================
def create_initial_complete_assignment(rng):
    assignment = {}

    for region in REGION_ORDER:
        assignment[region] = rng.choice(COLORS)

    return assignment


# =========================
# TÌM CÁC CẶP XUNG ĐỘT
# =========================
def get_conflicted_edges(assignment):
    conflicts = []

    for region in REGION_ORDER:
        for neighbor in ADJACENCY[region]:
            if region < neighbor and assignment[region] == assignment[neighbor]:
                conflicts.append((region, neighbor))

    return conflicts


def get_conflicted_variables(assignment):
    conflicted = set()

    for a, b in get_conflicted_edges(assignment):
        conflicted.add(a)
        conflicted.add(b)

    return sorted(list(conflicted))


# =========================
# CONFLICTS(var, value, current, csp)
# =========================
# Đếm số ràng buộc bị vi phạm nếu gán var = value.
# =========================
def count_conflicts_for_value(var, value, assignment):
    count = 0

    for neighbor in ADJACENCY[var]:
        if assignment[neighbor] == value:
            count += 1

    return count


def choose_min_conflict_value(var, assignment, rng):
    scores = {}

    for color in COLORS:
        scores[color] = count_conflicts_for_value(var, color, assignment)

    min_score = min(scores.values())

    best_colors = []

    for color in COLORS:
        if scores[color] == min_score:
            best_colors.append(color)

    # Nếu nhiều màu cùng ít xung đột nhất, chọn ngẫu nhiên một màu trong nhóm đó.
    chosen = rng.choice(best_colors)

    return chosen, scores


# =========================
# MIN-CONFLICTS SEARCH
# =========================
def minconflicts(max_steps=100, seed=None):
    # seed=None: mỗi lần chạy sẽ random khác nhau.
    rng = random.Random(seed)

    domains = create_domains()
    current = create_initial_complete_assignment(rng)
    steps = []

    initial_conflicts = get_conflicted_edges(current)

    add_step(
        steps,
        "start",
        None,
        None,
        current,
        domains,
        "Khởi tạo assignment ngẫu nhiên.",
        manual_log=[
            "current = " + format_assignment_short(current),
            "Xung đột ban đầu: " + format_conflicts(initial_conflicts)
        ],
        conflicts=initial_conflicts
    )

    for step_index in range(1, max_steps + 1):
        conflicts = get_conflicted_edges(current)

        if len(conflicts) == 0:
            add_step(
                steps,
                "done",
                None,
                None,
                current,
                domains,
                "Tìm được lời giải.",
                manual_log=[
                    "Không còn cặp vùng kề nào trùng màu.",
                    "Return solution."
                ],
                conflicts=conflicts
            )

            return {
                "success": True,
                "assignment": copy_assignment(current),
                "steps": steps,
                "regions": REGIONS,
                "colors": COLORS,
                "adjacency": ADJACENCY,
                "domains": domains
            }

        conflicted_variables = get_conflicted_variables(current)

        # Slide: var <- randomly chosen conflicted variable.
        var = rng.choice(conflicted_variables)

        chosen_value, scores = choose_min_conflict_value(var, current, rng)
        old_value = current[var]

        current[var] = chosen_value

        new_conflicts = get_conflicted_edges(current)

        add_step(
            steps,
            "assign",
            var,
            chosen_value,
            current,
            domains,
            "Sửa một vùng đang xung đột.",
            manual_log=[
                "Lặp " + str(step_index) + ": xung đột = " + format_conflicts(conflicts),
                "Chọn biến: " + REGION_CODES[var] + " (" + old_value + ")",
                "Điểm màu: " + format_scores(scores),
                "Cập nhật: " + REGION_CODES[var] + " = " + chosen_value,
                "Xung đột còn lại: " + format_conflicts(new_conflicts)
            ],
            scores=scores,
            conflicts=new_conflicts
        )

    add_step(
        steps,
        "failure",
        None,
        None,
        current,
        domains,
        "Vượt quá số bước cho phép.",
        manual_log=[
            "Không tìm được lời giải sau " + str(max_steps) + " bước.",
            "Return failure."
        ],
        conflicts=get_conflicted_edges(current)
    )

    return {
        "success": False,
        "assignment": None,
        "steps": steps,
        "regions": REGIONS,
        "colors": COLORS,
        "adjacency": ADJACENCY,
        "domains": domains
    }


def min_conflicts_search(max_steps=100, seed=None):
    return minconflicts(max_steps=max_steps, seed=seed)
