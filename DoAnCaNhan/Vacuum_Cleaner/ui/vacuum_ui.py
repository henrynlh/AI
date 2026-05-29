import tkinter as tk
from tkinter import ttk, messagebox
import time
import copy

from core.vacuum_problem import random_floor, format_floor
from algorithms.algorithm_manager import (
    solve,
    get_algorithm_names,
    get_search_types,
    get_no_type_algorithms,
    get_one_type_algorithms
)

class VacuumCleanerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Cleaner Search")
        self.root.geometry("1300x760")
        self.root.minsize(1100, 700)
        self.root.resizable(True, True)

        self.floor = None
        self.solution_steps = []
        self.current_step = -1
        self.is_running = False
        self.speed = 1000
        self.execution_time = 0

        self.grid_cache = {}

        self.setup_styles()
        self.setup_ui()

        # Khởi tạo trạng thái ban đầu mặc định
        self.load_default_state()

    # =========================
    # STYLE
    # =========================
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Sidebar.TFrame", background="#2C3E50")
        style.configure("Content.TFrame", background="#ECF0F1")
        style.configure("Panel.TFrame", background="#ECF0F1")
        style.configure("Box.TFrame", background="#FFFFFF")

        style.configure(
            "Title.TLabel",
            font=("Helvetica", 26, "bold"),
            background="#ECF0F1",
            foreground="#2C3E50"
        )

        style.configure(
            "PanelTitle.TLabel",
            font=("Helvetica", 16, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )

        style.configure(
            "Sidebar.TLabel",
            font=("Helvetica", 13, "bold"),
            background="#2C3E50",
            foreground="white"
        )

        style.configure(
            "Large.TButton",
            font=("Helvetica", 13, "bold"),
            padding=10
        )

    # =========================
    # SETUP UI
    # =========================
    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.setup_sidebar()
        self.setup_content()

    def setup_sidebar(self):
        self.sidebar = ttk.Frame(
            self.main_frame,
            width=300,
            style="Sidebar.TFrame"
        )
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="VACUUM AI",
            font=("Helvetica", 22, "bold"),
            bg="#2C3E50",
            fg="white"
        ).pack(pady=(22, 20))

        ttk.Label(self.sidebar, text="Số dòng", style="Sidebar.TLabel").pack(pady=(5, 3))
        self.row_entry = ttk.Entry(self.sidebar, font=("Helvetica", 13))
        self.row_entry.insert(0, "3")
        self.row_entry.pack(padx=25, pady=5, fill="x")

        ttk.Label(self.sidebar, text="Số cột", style="Sidebar.TLabel").pack(pady=(8, 3))
        self.col_entry = ttk.Entry(self.sidebar, font=("Helvetica", 13))
        self.col_entry.insert(0, "3")
        self.col_entry.pack(padx=25, pady=5, fill="x")

        ttk.Label(self.sidebar, text="Thuật toán", style="Sidebar.TLabel").pack(pady=(12, 3))
        algorithm_values = get_algorithm_names()
        self.algorithm_var = tk.StringVar(value=algorithm_values[0])
        self.algorithm_combobox = ttk.Combobox(
            self.sidebar,
            textvariable=self.algorithm_var,
            values=algorithm_values,
            state="readonly",
            font=("Helvetica", 12)
        )
        self.algorithm_combobox.pack(padx=25, pady=5, fill="x")
        self.algorithm_combobox.bind("<<ComboboxSelected>>", self.on_algorithm_change)

        # =========================
        # Dạng giải
        # Đặt trong frame riêng để dễ ẩn/hiện
        # =========================
        self.search_type_frame = tk.Frame(self.sidebar, bg="#2C3E50")

        ttk.Label(
            self.search_type_frame,
            text="Dạng giải",
            style="Sidebar.TLabel"
        ).pack(pady=(12, 3))

        search_type_values = get_search_types()
        self.search_type_var = tk.StringVar(value=search_type_values[0])
        self.search_type_combobox = ttk.Combobox(
            self.search_type_frame,
            textvariable=self.search_type_var,
            values=search_type_values,
            state="readonly",
            font=("Helvetica", 12)
        )
        self.search_type_combobox.pack(padx=25, pady=5, fill="x")

        self.search_type_frame.pack(fill="x")

        self.speed_label = ttk.Label(
            self.sidebar,
            text="Tốc độ chạy",
            style="Sidebar.TLabel"
        )
        self.speed_label.pack(pady=(12, 3))

        self.speed_scale = ttk.Scale(
            self.sidebar,
            from_=2000,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.on_speed_change
        )
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(padx=25, pady=5, fill="x")

        ttk.Button(
            self.sidebar,
            text="Random State",
            command=self.random_state,
            style="Large.TButton"
        ).pack(padx=25, pady=(20, 8), fill="x")

        ttk.Button(
            self.sidebar,
            text="Solve",
            command=self.solve_problem,
            style="Large.TButton"
        ).pack(padx=25, pady=8, fill="x")

        ttk.Button(
            self.sidebar,
            text="Stop",
            command=self.stop,
            style="Large.TButton"
        ).pack(padx=25, pady=8, fill="x")

        ttk.Button(
            self.sidebar,
            text="Reset",
            command=self.reset,
            style="Large.TButton"
        ).pack(padx=25, pady=8, fill="x")

        tk.Label(
            self.sidebar,
            text=(
                "Ký hiệu:\n"
                "0 = ô sạch\n"
                "1 = ô bẩn\n"
                "V = máy hút bụi"
            ),
            font=("Helvetica", 10),
            bg="#2C3E50",
            fg="white",
            justify="left"
        ).pack(pady=14, padx=25, anchor="w")

        self.on_algorithm_change()

    # =========================
    # ẨN / HIỆN DẠNG GIẢI THEO THUẬT TOÁN
    # =========================
    def on_algorithm_change(self, event=None):
        algorithm = self.algorithm_var.get()

        # Thuật toán không chia dạng thì ẩn Dạng giải
        if algorithm in get_no_type_algorithms():
            self.search_type_frame.pack_forget()

        else:
            # Nếu Dạng giải đang bị ẩn thì hiện lại
            if not self.search_type_frame.winfo_manager():
                self.search_type_frame.pack(
                    fill="x",
                    before=self.speed_label
                )

            # Thuật toán chỉ có Dạng 1, ví dụ UCS
            if algorithm in get_one_type_algorithms():
                self.search_type_combobox["values"] = ["Dạng 1"]
                self.search_type_var.set("Dạng 1")

            # Các thuật toán có Dạng 1 và Dạng 2
            else:
                search_type_values = get_search_types()
                self.search_type_combobox["values"] = search_type_values
                self.search_type_var.set(search_type_values[0])

    def setup_content(self):
        self.content_frame = ttk.Frame(
            self.main_frame,
            style="Content.TFrame"
        )
        self.content_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ttk.Label(
            self.content_frame,
            text="Vacuum Cleaner Search",
            style="Title.TLabel"
        ).pack(pady=(8, 4))

        self.info_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        self.info_frame.pack(pady=5)

        self.step_label = ttk.Label(
            self.info_frame,
            text="Step: 0",
            font=("Helvetica", 14, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.step_label.pack(side="left", padx=25)

        self.total_steps_label = ttk.Label(
            self.info_frame,
            text="Total steps: 0",
            font=("Helvetica", 14, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.total_steps_label.pack(side="left", padx=25)

        self.time_label = ttk.Label(
            self.info_frame,
            text="Time: 0s",
            font=("Helvetica", 14, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.time_label.pack(side="left", padx=25)

        self.body_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        self.body_frame.pack(fill="both", expand=True, padx=12, pady=10)

        self.body_frame.columnconfigure(0, weight=5, minsize=470)
        self.body_frame.columnconfigure(1, weight=7, minsize=470)
        self.body_frame.rowconfigure(0, weight=1)

        self.left_column = ttk.Frame(self.body_frame, style="Panel.TFrame")
        self.left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.right_column = ttk.Frame(self.body_frame, style="Panel.TFrame")
        self.right_column.grid(row=0, column=1, sticky="nsew")

        self.left_column.rowconfigure(0, weight=3, minsize=330)
        self.left_column.rowconfigure(1, weight=2, minsize=210)
        self.left_column.columnconfigure(0, weight=1)

        self.solve_steps_box = tk.Frame(
            self.left_column,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.solve_steps_box.grid(row=0, column=0, sticky="nsew", pady=(0, 8))

        ttk.Label(
            self.solve_steps_box,
            text="Các bước Solve",
            style="PanelTitle.TLabel"
        ).pack(pady=(8, 4))

        self.solve_grid_frame = tk.Frame(self.solve_steps_box, bg="#FFFFFF")
        self.solve_grid_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.result_box = tk.Frame(
            self.left_column,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.result_box.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

        ttk.Label(
            self.result_box,
            text="Trạng thái kết quả",
            style="PanelTitle.TLabel"
        ).pack(pady=(8, 4))

        self.result_grid_frame = tk.Frame(self.result_box, bg="#FFFFFF")
        self.result_grid_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.log_box = tk.Frame(
            self.right_column,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.log_box.pack(fill="both", expand=True)

        ttk.Label(
            self.log_box,
            text="Process Log",
            style="PanelTitle.TLabel"
        ).pack(pady=(8, 4))

        self.log_inner_frame = tk.Frame(self.log_box, bg="#FFFFFF")
        self.log_inner_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_scrollbar = ttk.Scrollbar(self.log_inner_frame, orient=tk.VERTICAL)

        self.log_text = tk.Text(
            self.log_inner_frame,
            height=28,
            width=70,
            font=("Consolas", 11),
            bg="#F9E79F",
            yscrollcommand=self.log_scrollbar.set,
            relief="flat",
            borderwidth=1
        )

        self.log_scrollbar.config(command=self.log_text.yview)
        self.log_scrollbar.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

    # =========================
    # DRAW GRID
    # =========================
    def get_cell_style(self, rows, cols, small=False):
        max_size = max(rows, cols)

        if small:
            if max_size <= 5:
                return 2, 1, 16, 2, 2
            if max_size <= 7:
                return 2, 1, 13, 1, 1
            if max_size <= 10:
                return 1, 1, 11, 1, 1
            return 1, 1, 9, 1, 1

        if max_size <= 4:
            return 4, 2, 22, 4, 4
        if max_size <= 5:
            return 4, 1, 22, 4, 4
        if max_size <= 7:
            return 3, 1, 18, 3, 3
        if max_size <= 10:
            return 2, 1, 14, 2, 2
        return 1, 1, 10, 1, 1

    def clear_grid(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        self.grid_cache.pop(parent_frame, None)

    def draw_grid(self, parent_frame, floor, small=False):
        if floor is None:
            self.clear_grid(parent_frame)
            return

        rows = len(floor)
        cols = len(floor[0])
        width, height, font_size, padx, pady = self.get_cell_style(rows, cols, small)
        style_key = (rows, cols, width, height, font_size, padx, pady)

        cached = self.grid_cache.get(parent_frame)

        if cached is None or cached.get("style_key") != style_key:
            self.clear_grid(parent_frame)

            grid_holder = tk.Frame(parent_frame, bg="#FFFFFF")
            grid_holder.pack(expand=True)

            labels = []
            for i in range(rows):
                row_labels = []
                for j in range(cols):
                    cell = tk.Label(
                        grid_holder,
                        text="",
                        width=width,
                        height=height,
                        font=("Helvetica", font_size, "bold"),
                        bg="#2ECC71",
                        fg="white",
                        relief="solid",
                        borderwidth=2
                    )
                    cell.grid(row=i, column=j, padx=padx, pady=pady)
                    row_labels.append(cell)
                labels.append(row_labels)

            self.grid_cache[parent_frame] = {
                "style_key": style_key,
                "labels": labels
            }
        else:
            labels = cached["labels"]

        for i in range(rows):
            for j in range(cols):
                value = floor[i][j]

                if value == "V":
                    bg = "#3498DB"
                    fg = "white"
                    text = "V"
                elif value == 1:
                    bg = "#E74C3C"
                    fg = "white"
                    text = "1"
                else:
                    bg = "#2ECC71"
                    fg = "white"
                    text = "0"

                labels[i][j].config(text=text, bg=bg, fg=fg)

    # =========================
    # BUTTON FUNCTIONS
    # =========================
    
        # =========================
    # LOAD TRẠNG THÁI MẶC ĐỊNH
    # =========================
    def load_default_state(self):
        self.is_running = False

        self.floor = [
            [1, 1, 0],
            ["V", 1, 0],
            [0, 1, 1]
        ]

        self.solution_steps = []
        self.current_step = -1
        self.execution_time = 0

        self.row_entry.delete(0, tk.END)
        self.row_entry.insert(0, "3")

        self.col_entry.delete(0, tk.END)
        self.col_entry.insert(0, "3")

        self.draw_grid(self.solve_grid_frame, self.floor)
        self.draw_grid(self.result_grid_frame, None)

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Đã tạo trạng thái ban đầu:\n")
        self.log_text.insert(tk.END, format_floor(self.floor) + "\n")

        self.step_label.config(text="Step: 0")
        self.total_steps_label.config(text="Total steps: 0")
        self.time_label.config(text="Time: 0s")
    
    def random_state(self):
        try:
            m = int(self.row_entry.get())
            n = int(self.col_entry.get())

            if m <= 0 or n <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Lỗi nhập dữ liệu",
                "Số dòng và số cột phải là số nguyên dương."
            )
            return

        self.is_running = False
        self.floor = random_floor(m, n)
        self.solution_steps = []
        self.current_step = -1

        self.draw_grid(self.solve_grid_frame, self.floor)
        self.draw_grid(self.result_grid_frame, None)

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Đã tạo trạng thái ban đầu:\n")
        self.log_text.insert(tk.END, format_floor(self.floor) + "\n")

        self.step_label.config(text="Step: 0")
        self.total_steps_label.config(text="Total steps: 0")
        self.time_label.config(text="Time: 0s")

    def solve_problem(self):
        if self.floor is None:
            messagebox.showwarning(
                "Thông báo",
                "Bạn cần bấm Random State trước."
            )
            return

        algorithm = self.algorithm_var.get()

        # Thuật toán không chia dạng thì không lấy search_type
        if algorithm in get_no_type_algorithms():
            search_type = None
            log_algorithm_name = algorithm
        else:
            search_type = self.search_type_var.get()
            log_algorithm_name = f"{algorithm} - {search_type}"

        self.log_text.insert(
            tk.END,
            f"\nBắt đầu giải bằng {log_algorithm_name}...\n"
        )
        self.log_text.see(tk.END)

        start_time = time.perf_counter()

        try:
            if search_type is None:
                result = solve(copy.deepcopy(self.floor), algorithm)
            else:
                result = solve(copy.deepcopy(self.floor), algorithm, search_type)

        except Exception as e:
            messagebox.showerror(
                "Lỗi khi giải",
                f"{log_algorithm_name} bị lỗi:\n{e}"
            )
            self.log_text.insert(tk.END, f"Lỗi: {e}\n")
            return

        end_time = time.perf_counter()
        self.execution_time = end_time - start_time

        if result is None:
            messagebox.showerror("Kết quả", "Không tìm thấy lời giải.")
            self.log_text.insert(tk.END, "Không tìm thấy lời giải.\n")
            return

        self.solution_steps = result["path"]
        self.current_step = -1
        self.is_running = True

        final_state = self.solution_steps[-1]
        self.draw_grid(self.result_grid_frame, final_state, small=True)

        self.total_steps_label.config(
            text=f"Total steps: {len(self.solution_steps) - 1}"
        )
        self.time_label.config(
            text=f"Time: {self.execution_time:.6f}s"
        )

        self.log_text.insert(
            tk.END,
            f"Đã tìm thấy lời giải bằng {log_algorithm_name}.\n"
        )
        self.log_text.insert(
            tk.END,
            f"Số bước đi: {len(self.solution_steps) - 1}\n"
        )
        self.log_text.insert(
            tk.END,
            f"Thời gian thực thi: {self.execution_time:.6f}s\n"
        )
        self.log_text.insert(
            tk.END,
            "\nTrạng thái kết quả:\n" + format_floor(final_state) + "\n"
        )

        self.auto_run_steps()

    def auto_run_steps(self):
        if not self.is_running:
            return

        if self.current_step < len(self.solution_steps) - 1:
            self.current_step += 1
            current_floor = self.solution_steps[self.current_step]

            self.draw_grid(self.solve_grid_frame, current_floor)
            self.step_label.config(text=f"Step: {self.current_step}")

            self.log_text.insert(
                tk.END,
                f"---\nTrạng thái {self.current_step}:\n"
            )
            self.log_text.insert(
                tk.END,
                format_floor(current_floor) + "\n"
            )
            self.log_text.see(tk.END)

            self.root.after(self.speed, self.auto_run_steps)
        else:
            self.is_running = False
            self.log_text.insert(
                tk.END,
                "---\nĐã hoàn thành quá trình tìm kiếm.\n"
            )
            self.log_text.see(tk.END)
            messagebox.showinfo(
                "Hoàn thành",
                "Máy hút bụi đã hút sạch toàn bộ ô bẩn."
            )

    def stop(self):
        self.is_running = False
        self.log_text.insert(tk.END, "\nĐã dừng bởi người dùng.\n")
        self.log_text.see(tk.END)

    def reset(self):
        self.is_running = False
        self.floor = None
        self.solution_steps = []
        self.current_step = -1
        self.execution_time = 0

        self.draw_grid(self.solve_grid_frame, None)
        self.draw_grid(self.result_grid_frame, None)

        self.log_text.delete(1.0, tk.END)

        self.step_label.config(text="Step: 0")
        self.total_steps_label.config(text="Total steps: 0")
        self.time_label.config(text="Time: 0s")

    def on_speed_change(self, value):
        # Kéo sang phải thì chạy nhanh hơn
        self.speed = int(float(value))