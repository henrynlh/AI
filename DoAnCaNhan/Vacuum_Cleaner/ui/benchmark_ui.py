# =========================
# BENCHMARK UI
# =========================
# Cửa sổ này dùng để chạy benchmark và sinh biểu đồ so sánh thuật toán.
# Phần này phục vụ báo cáo/thuyết trình, không thay thế visualizer thuật toán.
# =========================

import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from benchmark.benchmark_runner import run_all_benchmarks, DEFAULT_OUTPUT_CSV
from benchmark.chart_generator import generate_charts, DEFAULT_CHART_DIR


class BenchmarkUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Benchmark & Charts")
        self.root.geometry("900x620")
        self.root.minsize(820, 560)

        self.is_running = False
        self.last_csv_path = DEFAULT_OUTPUT_CSV
        self.last_chart_dir = DEFAULT_CHART_DIR

        self.setup_styles()
        self.setup_ui()

    # =========================
    # STYLE
    # =========================
    def setup_styles(self):
        style = ttk.Style()
        style.configure("BenchmarkTitle.TLabel", font=("Helvetica", 20, "bold"))
        style.configure("BenchmarkSub.TLabel", font=("Helvetica", 11))
        style.configure("BenchmarkButton.TButton", font=("Helvetica", 11, "bold"), padding=8)

    # =========================
    # SETUP UI
    # =========================
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=14)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame,
            text="So sánh thuật toán và tạo biểu đồ",
            style="BenchmarkTitle.TLabel"
        ).pack(anchor="w", pady=(0, 6))

        ttk.Label(
            main_frame,
            text=(
                "Chức năng này chạy benchmark trên các bài toán mẫu, xuất CSV và sinh biểu đồ PNG "
                "để đưa vào README hoặc báo cáo."
            ),
            style="BenchmarkSub.TLabel",
            wraplength=820
        ).pack(anchor="w", pady=(0, 12))

        option_frame = ttk.LabelFrame(main_frame, text="Cấu hình benchmark", padding=10)
        option_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(option_frame, text="Số lần chạy nhóm Local Search:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        self.local_run_var = tk.StringVar(value="10")
        self.local_run_entry = ttk.Entry(option_frame, textvariable=self.local_run_var, width=10)
        self.local_run_entry.grid(row=0, column=1, sticky="w", pady=4)

        ttk.Label(option_frame, text="Độ sâu tối đa nhóm đối kháng:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        self.depth_var = tk.StringVar(value="5")
        self.depth_entry = ttk.Entry(option_frame, textvariable=self.depth_var, width=10)
        self.depth_entry.grid(row=1, column=1, sticky="w", pady=4)

        note = (
            "Gợi ý: giữ Local Search = 10 và Depth = 5 để chạy nhanh. "
            "Nếu tăng quá cao, Minimax/Expectimax có thể chạy lâu hơn."
        )
        ttk.Label(option_frame, text=note, wraplength=780).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 12))

        self.run_button = ttk.Button(
            button_frame,
            text="Run Benchmark + Create Charts",
            command=self.run_benchmark_thread,
            style="BenchmarkButton.TButton"
        )
        self.run_button.pack(side="left", padx=(0, 8))

        ttk.Button(
            button_frame,
            text="Open Chart Folder",
            command=lambda: self.open_folder(self.last_chart_dir),
            style="BenchmarkButton.TButton"
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            button_frame,
            text="Open CSV Folder",
            command=lambda: self.open_folder(os.path.dirname(self.last_csv_path)),
            style="BenchmarkButton.TButton"
        ).pack(side="left")

        log_frame = ttk.LabelFrame(main_frame, text="Benchmark Log", padding=8)
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            log_frame,
            font=("Consolas", 10),
            bg="#F8F9F9",
            relief="flat",
            wrap="word"
        )
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

        self.write_log("Sẵn sàng chạy benchmark.\n")
        self.write_log("Output CSV: " + self.last_csv_path + "\n")
        self.write_log("Output charts: " + self.last_chart_dir + "\n")

    # =========================
    # GHI LOG
    # =========================
    def write_log(self, message):
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    # =========================
    # KIỂM TRA INPUT
    # =========================
    def get_options(self):
        try:
            local_run_count = int(self.local_run_var.get())
            adversarial_depth = int(self.depth_var.get())

            if local_run_count <= 0 or adversarial_depth <= 0:
                raise ValueError

            if adversarial_depth > 7:
                messagebox.showwarning(
                    "Cảnh báo",
                    "Depth lớn hơn 7 có thể làm Minimax/Expectimax chạy lâu. Nên dùng 5 hoặc 6 cho báo cáo."
                )

            return local_run_count, adversarial_depth

        except ValueError:
            messagebox.showerror(
                "Lỗi nhập dữ liệu",
                "Số lần chạy và độ sâu phải là số nguyên dương."
            )
            return None

    # =========================
    # CHẠY BẰNG THREAD ĐỂ UI KHÔNG ĐƠ
    # =========================
    def run_benchmark_thread(self):
        if self.is_running:
            messagebox.showinfo("Thông báo", "Benchmark đang chạy.")
            return

        options = self.get_options()
        if options is None:
            return

        local_run_count, adversarial_depth = options
        self.is_running = True
        self.run_button.config(state="disabled")

        thread = threading.Thread(
            target=self.run_benchmark,
            args=(local_run_count, adversarial_depth),
            daemon=True
        )
        thread.start()

    # =========================
    # CHẠY BENCHMARK + TẠO BIỂU ĐỒ
    # =========================
    def run_benchmark(self, local_run_count, adversarial_depth):
        try:
            self.write_log("\nBắt đầu benchmark...\n")
            self.write_log(f"Local Search runs = {local_run_count}\n")
            self.write_log(f"Adversarial max depth = {adversarial_depth}\n")

            csv_path = run_all_benchmarks(
                output_csv=self.last_csv_path,
                local_run_count=local_run_count,
                adversarial_max_depth=adversarial_depth
            )

            self.write_log("Đã xuất CSV: " + csv_path + "\n")
            self.write_log("Bắt đầu tạo biểu đồ...\n")

            chart_paths = generate_charts(
                csv_path=csv_path,
                output_dir=self.last_chart_dir
            )

            self.write_log("Đã tạo " + str(len(chart_paths)) + " biểu đồ:\n")
            for path in chart_paths:
                self.write_log("- " + path + "\n")

            self.write_log("\nHoàn thành benchmark và biểu đồ.\n")
            messagebox.showinfo("Hoàn thành", "Đã tạo CSV và biểu đồ benchmark.")

        except ModuleNotFoundError as exc:
            self.write_log("\nThiếu thư viện: " + str(exc) + "\n")
            self.write_log("Bạn cần cài matplotlib bằng lệnh: pip install matplotlib\n")
            messagebox.showerror("Thiếu thư viện", "Bạn cần cài matplotlib:\n\npip install matplotlib")

        except Exception as exc:
            self.write_log("\nLỗi benchmark: " + str(exc) + "\n")
            messagebox.showerror("Lỗi benchmark", str(exc))

        finally:
            self.is_running = False
            self.run_button.config(state="normal")

    # =========================
    # MỞ THƯ MỤC OUTPUT
    # =========================
    def open_folder(self, folder_path):
        os.makedirs(folder_path, exist_ok=True)

        try:
            if sys.platform.startswith("win"):
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder_path])
            else:
                subprocess.Popen(["xdg-open", folder_path])
        except Exception as exc:
            messagebox.showerror("Không mở được thư mục", str(exc))
