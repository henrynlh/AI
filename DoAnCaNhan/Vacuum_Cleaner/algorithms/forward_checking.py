# =========================
# FORWARD CHECKING
# MAP COLORING CSP
# =========================
# Bài toán:
# - Mỗi vùng trên bản đồ là 1 biến
# - Mỗi biến có miền giá trị là tập màu có thể chọn
# - Hai vùng kề nhau không được cùng màu
#
# Forward Checking:
# - Khi gán màu cho 1 vùng
# - Thuật toán nhìn trước sang các vùng kề chưa được gán
# - Xóa màu vừa gán khỏi miền giá trị của các vùng kề
# - Nếu có vùng nào bị rỗng miền màu thì quay lui ngay
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


COLORS = ["Đỏ", "Vàng", "Xanh lá", "Xanh dương"]


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


def create_initial_domains():
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


def is_valid_color(region, color, assignment):
    for neighbor in ADJACENCY[region]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False

    return True


def is_complete_assignment(assignment):
    return len(assignment) == len(REGION_ORDER)


def select_unassigned_region(assignment, domains):
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


def has_empty_domain(assignment, domains):
    for region in REGION_ORDER:
        if region not in assignment and len(domains[region]) == 0:
            return True

    return False


def get_empty_domains(assignment, domains):
    empty_regions = []

    for region in REGION_ORDER:
        if region not in assignment and len(domains[region]) == 0:
            empty_regions.append(region)

    return empty_regions


def forward_check(region, color, assignment, domains):
    new_domains = copy_domains(domains)
    removed_values = []

    for neighbor in ADJACENCY[region]:
        if neighbor not in assignment:
            if color in new_domains[neighbor]:
                new_domains[neighbor].remove(color)
                removed_values.append((neighbor, color))

    return new_domains, removed_values


def add_step(steps, step_type, region, color, assignment, domains, message, removed_values=None):
    if removed_values is None:
        removed_values = []

    step = {
        "type": step_type,
        "region": region,
        "region_name": REGIONS[region] if region is not None else "",
        "color": color,
        "assignment": copy_assignment(assignment),
        "domains": copy_domains(domains),
        "removed_values": removed_values.copy(),
        "message": message
    }

    steps.append(step)


def forward_checking_recursive(assignment, domains, steps):
    if is_complete_assignment(assignment):
        add_step(
            steps,
            "done",
            None,
            None,
            assignment,
            domains,
            "Hoàn thành: tất cả vùng đã được tô màu hợp lệ."
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
        f"Chọn biến {REGIONS[region]} vì còn miền màu: {{{', '.join(domains[region])}}}."
    )

    for color in domains[region].copy():
        add_step(
            steps,
            "try",
            region,
            color,
            assignment,
            domains,
            f"Thử gán {REGIONS[region]} = {color}."
        )

        if not is_valid_color(region, color, assignment):
            add_step(
                steps,
                "fail",
                region,
                color,
                assignment,
                domains,
                f"Không hợp lệ: {REGIONS[region]} = {color} bị trùng màu với vùng kề đã tô."
            )
            continue

        assignment[region] = color

        add_step(
            steps,
            "assign",
            region,
            color,
            assignment,
            domains,
            f"Hợp lệ: gán {REGIONS[region]} = {color}."
        )

        new_domains, removed_values = forward_check(region, color, assignment, domains)

        if len(removed_values) > 0:
            removed_texts = []

            for item in removed_values:
                neighbor = item[0]
                removed_color = item[1]
                removed_texts.append(f"xóa {removed_color} khỏi {REGIONS[neighbor]}")

            message = "Forward Checking: " + "; ".join(removed_texts) + "."
        else:
            message = "Forward Checking: không có miền nào cần cắt."

        add_step(
            steps,
            "forward_check",
            region,
            color,
            assignment,
            new_domains,
            message,
            removed_values
        )

        if has_empty_domain(assignment, new_domains):
            empty_regions = get_empty_domains(assignment, new_domains)
            empty_names = []

            for empty_region in empty_regions:
                empty_names.append(REGIONS[empty_region])

            add_step(
                steps,
                "domain_empty",
                region,
                color,
                assignment,
                new_domains,
                "Phát hiện domain rỗng tại: "
                + ", ".join(empty_names)
                + ". Nhánh này bị loại sớm."
            )

            del assignment[region]

            add_step(
                steps,
                "backtrack",
                region,
                color,
                assignment,
                domains,
                f"Quay lui: bỏ {REGIONS[region]} = {color} và khôi phục domain."
            )

            continue

        if forward_checking_recursive(assignment, new_domains, steps):
            return True

        del assignment[region]

        add_step(
            steps,
            "backtrack",
            region,
            color,
            assignment,
            domains,
            f"Quay lui: bỏ {REGIONS[region]} = {color} và thử màu khác."
        )

    return False


def forwardchecking():
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
        "Bắt đầu Forward Checking với assignment rỗng và domain ban đầu."
    )

    success = forward_checking_recursive(assignment, domains, steps)

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
            "Thất bại: không tìm được cách tô màu thỏa mãn ràng buộc."
        )

    result = {
        "success": success,
        "assignment": final_assignment,
        "steps": steps,
        "regions": REGIONS,
        "colors": COLORS,
        "adjacency": ADJACENCY,
        "domains": domains
    }

    return result
