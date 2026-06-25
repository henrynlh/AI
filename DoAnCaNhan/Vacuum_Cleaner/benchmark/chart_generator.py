# =========================
# CHART GENERATOR
# =========================
# File này đọc benchmark_results.csv và sinh các biểu đồ PNG để đưa vào README/báo cáo.
# Cần thư viện matplotlib:
#     pip install matplotlib
# =========================

import csv
import os
from collections import defaultdict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "reports", "benchmark_data", "benchmark_results.csv")
DEFAULT_CHART_DIR = os.path.join(BASE_DIR, "reports", "benchmark_charts")


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


# =========================
# TÍNH TRUNG BÌNH THEO THUẬT TOÁN
# =========================
def mean_by_algorithm(records, metric_name, filter_function=None):
    values = defaultdict(list)

    for record in records:
        if filter_function is not None and not filter_function(record):
            continue

        value = to_float(record.get(metric_name))
        if value is None:
            continue

        values[algorithm_label(record)].append(value)

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
# VẼ BAR CHART
# =========================
def create_bar_chart(data, title, y_label, output_path):
    import matplotlib.pyplot as plt

    if len(data) == 0:
        return None

    labels = [item[0] for item in data]
    values = [item[1] for item in data]

    plt.figure(figsize=(11, 6))
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xticks(rotation=30, ha="right")
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

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

    return output_path


# =========================
# FILTER NHÓM DỮ LIỆU
# =========================
def is_vacuum_path_algorithm(record):
    return (
        record.get("problem") == "Vacuum Cleaner"
        and record.get("group") in ["Tìm kiếm không có thông tin", "Tìm kiếm có thông tin"]
    )


def is_local_search(record):
    return record.get("group") == "Tìm kiếm cục bộ"


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

    chart_specs = [
        (
            mean_by_algorithm(records, "solution_steps", is_vacuum_path_algorithm),
            "So sánh số bước lời giải - Vacuum Cleaner",
            "Số bước lời giải trung bình",
            "01_vacuum_solution_steps.png"
        ),
        (
            mean_by_algorithm(records, "expanded_nodes", is_vacuum_path_algorithm),
            "So sánh số node mở rộng - Vacuum Cleaner",
            "Số node mở rộng trung bình",
            "02_vacuum_expanded_nodes.png"
        ),
        (
            mean_by_algorithm(records, "runtime_ms", is_vacuum_path_algorithm),
            "So sánh thời gian chạy - Vacuum Cleaner",
            "Thời gian chạy trung bình (ms)",
            "03_vacuum_runtime_ms.png"
        ),
        (
            success_rate_by_algorithm(records, is_local_search),
            "Tỷ lệ thành công - Tìm kiếm cục bộ",
            "Tỷ lệ thành công (%)",
            "04_local_success_rate.png"
        ),
        (
            mean_by_algorithm(records, "final_dirty_cells", is_local_search),
            "Số ô bẩn còn lại trung bình - Tìm kiếm cục bộ",
            "Số ô bẩn còn lại trung bình",
            "05_local_final_dirty_cells.png"
        ),
        (
            mean_by_algorithm(records, "backtracks", is_csp),
            "So sánh số lần quay lui - CSP Map Coloring",
            "Số lần quay lui",
            "06_csp_backtracks.png"
        ),
        (
            mean_by_algorithm(records, "assignments", is_csp),
            "So sánh số lần gán giá trị - CSP Map Coloring",
            "Số lần gán màu",
            "07_csp_assignments.png"
        ),
        (
            mean_by_algorithm(records, "expanded_nodes", is_adversarial_depth_5),
            "Số node mở rộng - Thuật toán đối kháng",
            "Số node mở rộng ở depth = 5",
            "08_adversarial_expanded_nodes_depth5.png"
        ),
        (
            mean_by_algorithm(records, "runtime_ms", is_adversarial_depth_5),
            "Thời gian chạy - Thuật toán đối kháng",
            "Thời gian chạy ở depth = 5 (ms)",
            "09_adversarial_runtime_depth5.png"
        ),
    ]

    for data, title, y_label, filename in chart_specs:
        chart_path = os.path.join(output_dir, filename)
        created_path = create_bar_chart(data, title, y_label, chart_path)
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

    return chart_paths


# =========================
# CHẠY TRỰC TIẾP BẰNG TERMINAL
# =========================
if __name__ == "__main__":
    paths = generate_charts()
    print("Đã tạo biểu đồ:")
    for path in paths:
        print("-", path)