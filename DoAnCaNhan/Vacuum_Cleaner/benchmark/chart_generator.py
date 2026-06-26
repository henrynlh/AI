# =========================
# CHART GENERATOR
# =========================
# File này đọc benchmark_results.csv và sinh các biểu đồ PNG để đưa vào README/báo cáo.
# Cần thư viện matplotlib:
#     pip install matplotlib
#
# Bản cập nhật:
# - Vẫn giữ các biểu đồ đơn cũ để không làm hỏng README hiện tại.
# - Bổ sung biểu đồ so sánh theo từng nhóm thuật toán.
# - Mỗi nhóm có 3 sơ đồ: Thời gian, Số trạng thái đã thăm, Bộ nhớ sử dụng.
# - Màu lần lượt: đỏ, xanh, vàng.
# =========================

import csv
import os
import textwrap
from collections import defaultdict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "reports", "benchmark_data", "benchmark_results.csv")
DEFAULT_CHART_DIR = os.path.join(BASE_DIR, "reports", "benchmark_charts")

# Màu theo yêu cầu:
# 1. Thời gian: đỏ
# 2. Số trạng thái đã thăm: xanh
# 3. Bộ nhớ sử dụng: vàng
TIME_COLOR = "#e74c3c"
VISITED_COLOR = "#2ecc71"
MEMORY_COLOR = "#f1c40f"


# =========================
# ĐỌC CSV
# =========================
def read_records(csv_path):
    with open(csv_path, "r", encoding="utf-8-sig") as csv_file:
        return list(csv.DictReader(csv_file))


# =========================
# CHUYỂN SỐ AN TOÀN
# =========================
def to_float(value):
    try:
        if value is None or value == "":
            return None
        return float(value)
    except ValueError:
        return None


# =========================
# TẠO NHÃN THUẬT TOÁN
# =========================
def algorithm_label(record):
    algorithm = record.get("algorithm", "")
    search_type = record.get("search_type", "")

    if search_type:
        return algorithm + "\n" + search_type

    return algorithm


def short_algorithm_label(record):
    label = algorithm_label(record)

    replacements = {
        "Simple Hill Climbing": "Simple HC",
        "Steepest Ascent Hill Climbing": "Steepest HC",
        "Stochastic Hill Climbing": "Stochastic HC",
        "Random Restart Hill Climbing": "Random Restart HC",
        "Local Beam Search": "Local Beam",
        "Simulated Annealing": "SA",
        "No Observation Search": "No Observation",
        "Partial Observation Search": "Partial Observation",
        "AND-OR Graph Search": "AND-OR",
        "Alpha-Beta Pruning": "Alpha-Beta",
        "Forward Checking": "Forward Checking",
        "Min-Conflicts": "Min-Conflicts",
    }

    return replacements.get(label, label)


# =========================
# TÍNH TRUNG BÌNH THEO THUẬT TOÁN
# =========================
def mean_by_algorithm(records, metric_name, filter_function=None, use_short_label=False):
    values = defaultdict(list)

    for record in records:
        if filter_function is not None and not filter_function(record):
            continue

        value = to_float(record.get(metric_name))
        if value is None:
            continue

        label = short_algorithm_label(record) if use_short_label else algorithm_label(record)
        values[label].append(value)

    result = []
    for label, items in values.items():
        if len(items) == 0:
            continue
        result.append((label, sum(items) / len(items)))

    return result


# =========================
# TỶ LỆ THÀNH CÔNG THEO THUẬT TOÁN
# =========================
def success_rate_by_algorithm(records, filter_function=None):
    total = defaultdict(int)
    success = defaultdict(int)

    for record in records:
        if filter_function is not None and not filter_function(record):
            continue

        label = algorithm_label(record)
        total[label] += 1

        if str(record.get("success", "")).lower() == "true":
            success[label] += 1

    result = []
    for label in total:
        if total[label] == 0:
            continue
        result.append((label, success[label] * 100 / total[label]))

    return result


# =========================
# VẼ BAR CHART ĐƠN
# =========================
def create_bar_chart(data, title, y_label, output_path, color="#1f77b4"):
    import matplotlib.pyplot as plt

    if len(data) == 0:
        return None

    labels = [item[0] for item in data]
    values = [item[1] for item in data]

    plt.figure(figsize=(11, 6))
    plt.bar(labels, values, color=color)
    plt.title(title, fontsize=13, fontweight="bold")
    plt.ylabel(y_label)
    plt.xticks(rotation=30, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

    return output_path


# =========================
# VẼ LINE CHART
# =========================
def create_line_chart(series_data, title, x_label, y_label, output_path):
    import matplotlib.pyplot as plt

    if len(series_data) == 0:
        return None

    plt.figure(figsize=(11, 6))

    for algorithm, points in series_data.items():
        points = sorted(points, key=lambda item: item[0])
        x_values = [item[0] for item in points]
        y_values = [item[1] for item in points]
        plt.plot(x_values, y_values, marker="o", label=algorithm)

    plt.title(title, fontsize=13, fontweight="bold")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

    return output_path


# =========================
# HỖ TRỢ VẼ NHÓM 3 SƠ ĐỒ
# =========================
def wrap_labels(labels, width=14):
    wrapped = []
    for label in labels:
        parts = str(label).split("\n")
        wrapped_parts = []
        for part in parts:
            wrapped_parts.append("\n".join(textwrap.wrap(part, width=width)) or part)
        wrapped.append("\n".join(wrapped_parts))
    return wrapped


def add_value_labels(axis, bars, values):
    max_value = max(values) if values else 0
    offset = max_value * 0.02 if max_value > 0 else 0.1

    for bar, value in zip(bars, values):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + offset,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=8
        )


def get_metric_data(records, metric_name, filter_function):
    data = mean_by_algorithm(
        records,
        metric_name,
        filter_function=filter_function,
        use_short_label=True
    )
    return data


def create_three_metric_group_chart(records, group_title, filter_function, output_path):
    import matplotlib.pyplot as plt

    time_data = get_metric_data(records, "runtime_ms", filter_function)
    visited_data = get_metric_data(records, "expanded_nodes", filter_function)
    memory_data = get_metric_data(records, "memory_kb", filter_function)

    # Nếu CSV cũ chưa có memory_kb thì fallback sang generated_nodes để vẫn vẽ được.
    if len(memory_data) == 0:
        memory_data = get_metric_data(records, "generated_nodes", filter_function)
        memory_label = "Bộ nhớ ước lượng\n(generated nodes)"
    else:
        memory_label = "Bộ nhớ sử dụng\n(KiB)"

    if len(time_data) == 0 and len(visited_data) == 0 and len(memory_data) == 0:
        return None

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.6))
    fig.suptitle(group_title, fontsize=16, fontweight="bold")

    chart_items = [
        (axes[0], time_data, "Thời gian", "Thời gian chạy (ms)", TIME_COLOR),
        (axes[1], visited_data, "Số trạng thái đã thăm", "Số node mở rộng", VISITED_COLOR),
        (axes[2], memory_data, "Bộ nhớ sử dụng", memory_label, MEMORY_COLOR),
    ]

    for axis, data, title, y_label, color in chart_items:
        if len(data) == 0:
            axis.set_title(title, fontweight="bold")
            axis.text(0.5, 0.5, "Không có dữ liệu", ha="center", va="center")
            axis.axis("off")
            continue

        labels = [item[0] for item in data]
        values = [item[1] for item in data]
        x_positions = list(range(len(labels)))

        bars = axis.bar(x_positions, values, color=color, edgecolor="#333333", linewidth=0.7)
        axis.set_title(title, fontweight="bold")
        axis.set_ylabel(y_label)
        axis.set_xticks(x_positions)
        axis.set_xticklabels(wrap_labels(labels), rotation=0, fontsize=8)
        axis.grid(axis="y", linestyle="--", alpha=0.3)
        add_value_labels(axis, bars, values)

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(output_path, dpi=170)
    plt.close()

    return output_path


# =========================
# FILTER NHÓM DỮ LIỆU
# =========================
def is_group(group_name):
    return lambda record: record.get("group") == group_name


def is_vacuum_path_algorithm(record):
    return (
        record.get("problem") == "Vacuum Cleaner"
        and record.get("group") in ["Tìm kiếm không có thông tin", "Tìm kiếm có thông tin"]
    )


def is_local_search(record):
    return record.get("group") == "Tìm kiếm cục bộ"


def is_complex_environment(record):
    return record.get("group") == "Môi trường phức tạp"


def is_csp(record):
    return record.get("group") == "Ràng buộc CSP"


def is_adversarial_depth_5(record):
    return record.get("group") == "Đối kháng" and str(record.get("depth")) == "5"


def is_adversarial(record):
    return record.get("group") == "Đối kháng"


# =========================
# TẠO TOÀN BỘ BIỂU ĐỒ
# =========================
def generate_charts(csv_path=DEFAULT_CSV_PATH, output_dir=DEFAULT_CHART_DIR):
    os.makedirs(output_dir, exist_ok=True)
    records = read_records(csv_path)
    chart_paths = []

    # =========================
    # BIỂU ĐỒ ĐƠN CŨ
    # =========================
    # Giữ lại để README hoặc báo cáo cũ vẫn không bị lỗi đường dẫn.
    chart_specs = [
        (
            mean_by_algorithm(records, "solution_steps", is_vacuum_path_algorithm),
            "So sánh số bước lời giải - Vacuum Cleaner",
            "Số bước lời giải trung bình",
            "01_vacuum_solution_steps.png",
            "#1f77b4"
        ),
        (
            mean_by_algorithm(records, "expanded_nodes", is_vacuum_path_algorithm),
            "So sánh số node mở rộng - Vacuum Cleaner",
            "Số node mở rộng trung bình",
            "02_vacuum_expanded_nodes.png",
            "#1f77b4"
        ),
        (
            mean_by_algorithm(records, "runtime_ms", is_vacuum_path_algorithm),
            "So sánh thời gian chạy - Vacuum Cleaner",
            "Thời gian chạy trung bình (ms)",
            "03_vacuum_runtime_ms.png",
            "#1f77b4"
        ),
        (
            success_rate_by_algorithm(records, is_local_search),
            "Tỷ lệ thành công - Tìm kiếm cục bộ",
            "Tỷ lệ thành công (%)",
            "04_local_success_rate.png",
            "#1f77b4"
        ),
        (
            mean_by_algorithm(records, "final_dirty_cells", is_local_search),
            "Số ô bẩn còn lại trung bình - Tìm kiếm cục bộ",
            "Số ô bẩn còn lại trung bình",
            "05_local_final_dirty_cells.png",
            "#1f77b4"
        ),
        (
            mean_by_algorithm(records, "backtracks", is_csp),
            "So sánh số lần quay lui - CSP Map Coloring",
            "Số lần quay lui",
            "06_csp_backtracks.png",
            "#1f77b4"
        ),
        (
            mean_by_algorithm(records, "assignments", is_csp),
            "So sánh số lần gán giá trị - CSP Map Coloring",
            "Số lần gán màu",
            "07_csp_assignments.png",
            "#1f77b4"
        ),
        (
            mean_by_algorithm(records, "expanded_nodes", is_adversarial_depth_5),
            "Số node mở rộng - Thuật toán đối kháng",
            "Số node mở rộng ở depth = 5",
            "08_adversarial_expanded_nodes_depth5.png",
            "#1f77b4"
        ),
        (
            mean_by_algorithm(records, "runtime_ms", is_adversarial_depth_5),
            "Thời gian chạy - Thuật toán đối kháng",
            "Thời gian chạy ở depth = 5 (ms)",
            "09_adversarial_runtime_depth5.png",
            "#1f77b4"
        ),
    ]

    for data, title, y_label, filename, color in chart_specs:
        chart_path = os.path.join(output_dir, filename)
        created_path = create_bar_chart(data, title, y_label, chart_path, color=color)
        if created_path is not None:
            chart_paths.append(created_path)

    # Biểu đồ line: depth -> expanded_nodes cho nhóm đối kháng.
    series_data = defaultdict(list)

    for record in records:
        if not is_adversarial(record):
            continue

        depth = to_float(record.get("depth"))
        expanded_nodes = to_float(record.get("expanded_nodes"))

        if depth is None or expanded_nodes is None:
            continue

        series_data[record.get("algorithm")].append((depth, expanded_nodes))

    line_chart_path = os.path.join(output_dir, "10_adversarial_expanded_nodes_by_depth.png")
    created_path = create_line_chart(
        series_data,
        "Số node mở rộng theo độ sâu - Thuật toán đối kháng",
        "Độ sâu tìm kiếm",
        "Số node mở rộng",
        line_chart_path
    )
    if created_path is not None:
        chart_paths.append(created_path)

    # =========================
    # BIỂU ĐỒ MỚI THEO NHÓM
    # =========================
    group_chart_specs = [
        (
            "So sánh nhóm Tìm kiếm không có thông tin",
            is_group("Tìm kiếm không có thông tin"),
            "11_group_uninformed_three_metrics.png"
        ),
        (
            "So sánh nhóm Tìm kiếm có thông tin",
            is_group("Tìm kiếm có thông tin"),
            "12_group_informed_three_metrics.png"
        ),
        (
            "So sánh nhóm Tìm kiếm cục bộ",
            is_group("Tìm kiếm cục bộ"),
            "13_group_local_search_three_metrics.png"
        ),
        (
            "So sánh nhóm Môi trường phức tạp",
            is_complex_environment,
            "14_group_complex_environment_three_metrics.png"
        ),
        (
            "So sánh nhóm Ràng buộc CSP",
            is_csp,
            "15_group_csp_three_metrics.png"
        ),
        (
            "So sánh nhóm Đối kháng ở độ sâu 5",
            is_adversarial_depth_5,
            "16_group_adversarial_three_metrics.png"
        ),
    ]

    for title, filter_function, filename in group_chart_specs:
        chart_path = os.path.join(output_dir, filename)
        created_path = create_three_metric_group_chart(
            records,
            title,
            filter_function,
            chart_path
        )
        if created_path is not None:
            chart_paths.append(created_path)

    return chart_paths


# =========================
# CHẠY TRỰC TIẾP BẰNG TERMINAL
# =========================
if __name__ == "__main__":
    paths = generate_charts()
    print("Đã tạo biểu đồ:")
    for path in paths:
        print("-", path)
