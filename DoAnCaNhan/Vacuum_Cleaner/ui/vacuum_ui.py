import tkinter as tk
from tkinter import ttk, messagebox
import time
import copy

from core.vacuum_problem import random_floor, format_floor
from ui.map_coloring_ui import MapColoringUI

from algorithms.no_observation_search import (
    create_initial_belief_state as create_no_observation_initial_belief_state,
    count_wrong_cells_in_belief,
    manhattan_distance_in_belief
)
from algorithms.partial_observation_search import (
    create_initial_belief_state as create_partial_observation_initial_belief_state
)

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

        self.belief_initial_state = None
        self.belief_actions = []
        self.observed_positions = set()

        self.grid_cache = {}
        
        self.map_coloring_window = None
        self.map_coloring_app = None

        self.setup_styles()
        self.setup_ui()

        # Khởi tạo trạng thái ban đầu mặc định
        self.load_default_state()
        

    def open_map_coloring_window(self, algorithm_name):
        if self.map_coloring_window is not None and self.map_coloring_window.winfo_exists():
            self.map_coloring_app.set_algorithm(algorithm_name)
            self.map_coloring_window.lift()
            self.map_coloring_window.focus_force()
            return

        self.map_coloring_window = tk.Toplevel(self.root)
        self.map_coloring_app = MapColoringUI(
            self.map_coloring_window,
            algorithm_name
        )

        def on_close():
            self.map_coloring_window.destroy()
            self.map_coloring_window = None
            self.map_coloring_app = None

        self.map_coloring_window.protocol("WM_DELETE_WINDOW", on_close)
        
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
    # KIỂM TRA THUẬT TOÁN BELIEF SEARCH
    # =========================
    def is_no_observation_algorithm(self):
        return self.algorithm_var.get() == "No Observation Search"

    def is_partial_observation_algorithm(self):
        return self.algorithm_var.get() == "Partial Observation Search"

    def is_belief_algorithm(self):
        return self.is_no_observation_algorithm() or self.is_partial_observation_algorithm()

    # =========================
    # ẨN / HIỆN DẠNG GIẢI THEO THUẬT TOÁN
    # =========================
    def on_algorithm_change(self, event=None):
        algorithm = self.algorithm_var.get()
        
        # Nếu chọn thuật toán Backtracking hay Forward Checking
        # thì mở cửa sổ mô phỏng tô màu bản đồ ngay
        if algorithm in ["Map Coloring Backtracking", "Forward Checking"]:
            self.open_map_coloring_window(algorithm)

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

        # Khi đã tạo xong phần content thì cập nhật lại 2 khung hiển thị
        if hasattr(self, "solve_grid_frame"):
            self.update_panel_titles()

            if self.floor is not None:
                self.is_running = False
                self.solution_steps = []
                self.current_step = -1

                if self.is_no_observation_algorithm():
                    self.prepare_belief_initial_state()
                    self.draw_belief_grid(self.solve_grid_frame, self.belief_initial_state)
                    self.draw_grid(self.result_grid_frame, None)
                elif self.is_partial_observation_algorithm():
                    self.observed_positions = set()
                    self.belief_initial_state = None
                    self.draw_observable_grid(self.solve_grid_frame, self.floor)
                    self.draw_grid(self.result_grid_frame, None)
                else:
                    self.draw_grid(self.solve_grid_frame, self.floor)
                    self.draw_grid(self.result_grid_frame, None)

                self.step_label.config(text="Step: 0")
                self.total_steps_label.config(text="Total steps: 0")
                self.time_label.config(text="Time: 0s")

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

        self.solve_title_label = ttk.Label(
            self.solve_steps_box,
            text="Các bước Solve",
            style="PanelTitle.TLabel"
        )
        self.solve_title_label.pack(pady=(8, 4))

        self.solve_grid_frame = tk.Frame(self.solve_steps_box, bg="#FFFFFF")
        self.solve_grid_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.result_box = tk.Frame(
            self.left_column,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.result_box.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

        self.result_title_label = ttk.Label(
            self.result_box,
            text="Trạng thái kết quả",
            style="PanelTitle.TLabel"
        )
        self.result_title_label.pack(pady=(8, 4))

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
    # ĐỔI TIÊU ĐỀ 2 KHUNG THEO THUẬT TOÁN
    # =========================
    def update_panel_titles(self):
        if self.is_no_observation_algorithm():
            self.solve_title_label.config(text="Belief State ban đầu")
            self.result_title_label.config(text="Các bước Solve")
        elif self.is_partial_observation_algorithm():
            self.solve_title_label.config(text="Random State - Ctrl + Click chọn ô nhìn thấy")
            self.result_title_label.config(text="Belief states có thể xảy ra / Các bước Solve")
        else:
            self.solve_title_label.config(text="Các bước Solve")
            self.result_title_label.config(text="Trạng thái kết quả")

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
    # VẼ RANDOM STATE CHO PARTIAL OBSERVATION
    # Người dùng Ctrl + Click để chọn ô được nhìn thấy
    # =========================
    def draw_observable_grid(self, parent_frame, floor):
        if floor is None:
            self.clear_grid(parent_frame)
            return

        self.clear_grid(parent_frame)

        rows = len(floor)
        cols = len(floor[0])
        width, height, font_size, padx, pady = self.get_cell_style(rows, cols)

        holder = tk.Frame(parent_frame, bg="#FFFFFF")
        holder.pack(expand=True)

        note = tk.Label(
            holder,
            text="Ctrl + Click vào ô để chọn/bỏ chọn ô được nhìn thấy",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#34495E"
        )
        note.grid(row=0, column=0, columnspan=cols, pady=(0, 6))

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

                if (i, j) in self.observed_positions:
                    highlight_color = "#F1C40F"
                    highlight_size = 4
                else:
                    highlight_color = "#000000"
                    highlight_size = 1

                cell = tk.Label(
                    holder,
                    text=text,
                    width=width,
                    height=height,
                    font=("Helvetica", font_size, "bold"),
                    bg=bg,
                    fg=fg,
                    relief="solid",
                    borderwidth=2,
                    highlightbackground=highlight_color,
                    highlightcolor=highlight_color,
                    highlightthickness=highlight_size
                )
                cell.grid(row=i + 1, column=j, padx=padx, pady=pady)
                cell.bind(
                    "<Control-Button-1>",
                    lambda event, row=i, col=j: self.toggle_observed_cell(row, col)
                )

        selected_text = self.get_observed_text()
        selected_label = tk.Label(
            holder,
            text=selected_text,
            font=("Helvetica", 10),
            bg="#FFFFFF",
            fg="#34495E"
        )
        selected_label.grid(row=rows + 1, column=0, columnspan=cols, pady=(6, 0))

    # =========================
    # CHỌN / BỎ CHỌN Ô ĐƯỢC QUAN SÁT
    # =========================
    def toggle_observed_cell(self, row, col):
        position = (row, col)

        if position in self.observed_positions:
            self.observed_positions.remove(position)
        else:
            self.observed_positions.add(position)

        self.draw_observable_grid(self.solve_grid_frame, self.floor)

        # Với Partial Observation Search:
        # sau khi chọn ô nhìn thấy thì random 2 trạng thái có thể xảy ra
        # từ các ô đang được nhìn thấy và hiển thị ở khung phía dưới
        if self.is_partial_observation_algorithm():
            if len(self.observed_positions) > 0:
                self.belief_initial_state = create_partial_observation_initial_belief_state(
                    copy.deepcopy(self.floor),
                    sorted(list(self.observed_positions)),
                    state_count=2
                )
                self.draw_belief_grid(self.result_grid_frame, self.belief_initial_state, small=True)
            else:
                self.belief_initial_state = None
                self.draw_grid(self.result_grid_frame, None)

        self.log_text.insert(
            tk.END,
            "\nCác ô đang được nhìn thấy: " + self.get_observed_text() + "\n"
        )

        if self.is_partial_observation_algorithm() and self.belief_initial_state is not None:
            self.log_text.insert(
                tk.END,
                "2 belief states có thể xảy ra:\n" + self.format_belief_state(self.belief_initial_state) + "\n"
            )

        self.log_text.see(tk.END)

    # =========================
    # FORMAT DANH SÁCH Ô ĐƯỢC QUAN SÁT
    # =========================
    def get_observed_text(self):
        if len(self.observed_positions) == 0:
            return "Chưa chọn ô nhìn thấy"

        positions = sorted(list(self.observed_positions))
        texts = []

        for i, j in positions:
            texts.append(f"({i + 1},{j + 1})")

        return "Ô nhìn thấy: " + ", ".join(texts)

    # =========================
    # VẼ 1 MA TRẬN NHỎ TRONG BELIEF_STATE
    # =========================
    def draw_single_state_grid(self, parent_frame, floor, small=False):
        rows = len(floor)
        cols = len(floor[0])
        width, height, font_size, padx, pady = self.get_cell_style(rows, cols, small)

        grid_holder = tk.Frame(parent_frame, bg="#FFFFFF")
        grid_holder.pack(expand=True)

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

                cell = tk.Label(
                    grid_holder,
                    text=text,
                    width=width,
                    height=height,
                    font=("Helvetica", font_size, "bold"),
                    bg=bg,
                    fg=fg,
                    relief="solid",
                    borderwidth=2
                )
                cell.grid(row=i, column=j, padx=padx, pady=pady)

    # =========================
    # VẼ BELIEF_STATE GỒM 2 MA TRẬN NẰM NGANG
    # =========================
    def draw_belief_grid(self, parent_frame, belief_state, small=False):
        if belief_state is None:
            self.clear_grid(parent_frame)
            return

        self.clear_grid(parent_frame)

        holder = tk.Frame(parent_frame, bg="#FFFFFF")
        holder.pack(expand=True)

        for index, state in enumerate(belief_state):
            state_frame = tk.Frame(holder, bg="#FFFFFF")
            state_frame.grid(row=0, column=index, padx=12, pady=6)

            title = tk.Label(
                state_frame,
                text=f"State {index + 1}",
                font=("Helvetica", 11, "bold"),
                bg="#FFFFFF",
                fg="#34495E"
            )
            title.pack(pady=(0, 3))

            self.draw_single_state_grid(state_frame, state, small=small)

        g_value = count_wrong_cells_in_belief(belief_state)
        h_value = manhattan_distance_in_belief(belief_state)
        f_value = g_value + h_value

        info = tk.Label(
            holder,
            text=f"g(n)={g_value}   h(n)={h_value}   f(n)={f_value}",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#34495E"
        )
        info.grid(row=1, column=0, columnspan=len(belief_state), pady=(6, 0))

    # =========================
    # FORMAT BELIEF_STATE ĐỂ GHI LOG
    # =========================
    def format_belief_state(self, belief_state):
        text = ""

        for index, state in enumerate(belief_state):
            text += f"State {index + 1}:\n"
            text += format_floor(state) + "\n"

        return text

    # =========================
    # TẠO BELIEF_STATE BAN ĐẦU TỪ FLOOR HIỆN TẠI
    # =========================
    def prepare_belief_initial_state(self):
        if self.belief_initial_state is None:
            self.belief_initial_state = create_no_observation_initial_belief_state(copy.deepcopy(self.floor))

    # =========================
    # TẠO 2 BELIEF_STATE BAN ĐẦU CHO PARTIAL OBSERVATION
    # =========================
    def prepare_partial_belief_initial_state(self):
        self.belief_initial_state = create_partial_observation_initial_belief_state(
            copy.deepcopy(self.floor),
            sorted(list(self.observed_positions)),
            state_count=2
        )

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
        self.belief_initial_state = None
        self.belief_actions = []
        self.observed_positions = set()

        self.row_entry.delete(0, tk.END)
        self.row_entry.insert(0, "3")

        self.col_entry.delete(0, tk.END)
        self.col_entry.insert(0, "3")

        self.update_panel_titles()

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Đã tạo trạng thái ban đầu:\n")

        if self.is_no_observation_algorithm():
            self.prepare_belief_initial_state()
            self.draw_belief_grid(self.solve_grid_frame, self.belief_initial_state)
            self.draw_grid(self.result_grid_frame, None)
            self.log_text.insert(tk.END, self.format_belief_state(self.belief_initial_state) + "\n")
        elif self.is_partial_observation_algorithm():
            self.draw_observable_grid(self.solve_grid_frame, self.floor)
            self.draw_grid(self.result_grid_frame, None)
            self.log_text.insert(tk.END, format_floor(self.floor) + "\n")
            self.log_text.insert(tk.END, "Ctrl + Click vào ô muốn cho thuật toán nhìn thấy.\n")
        else:
            self.draw_grid(self.solve_grid_frame, self.floor)
            self.draw_grid(self.result_grid_frame, None)
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
        self.solution_steps = []
        self.current_step = -1
        self.execution_time = 0
        self.belief_actions = []
        self.observed_positions = set()

        self.log_text.delete(1.0, tk.END)

        if self.is_no_observation_algorithm():
            # No Observation Search dùng 2 trạng thái ban đầu
            # nên Random State sẽ tạo 2 ma trận ngẫu nhiên
            state_1 = random_floor(m, n)
            state_2 = random_floor(m, n)

            self.floor = copy.deepcopy(state_1)
            self.belief_initial_state = [state_1, state_2]

            self.draw_belief_grid(self.solve_grid_frame, self.belief_initial_state)
            self.draw_grid(self.result_grid_frame, None)

            self.log_text.insert(tk.END, "Đã tạo 2 belief states ban đầu:\n")
            self.log_text.insert(tk.END, self.format_belief_state(self.belief_initial_state) + "\n")
        elif self.is_partial_observation_algorithm():
            # Partial Observation Search dùng 1 random state thật
            # Sau đó người dùng Ctrl + Click chọn các ô được nhìn thấy
            self.floor = random_floor(m, n)
            self.belief_initial_state = None
            self.observed_positions = set()

            self.draw_observable_grid(self.solve_grid_frame, self.floor)
            self.draw_grid(self.result_grid_frame, None)

            self.log_text.insert(tk.END, "Đã tạo random state thật cho Partial Observation Search:\n")
            self.log_text.insert(tk.END, format_floor(self.floor) + "\n")
            self.log_text.insert(tk.END, "Ctrl + Click vào các ô được nhìn thấy rồi bấm Solve.\n")
        else:
            self.floor = random_floor(m, n)
            self.belief_initial_state = None

            self.draw_grid(self.solve_grid_frame, self.floor)
            self.draw_grid(self.result_grid_frame, None)

            self.log_text.insert(tk.END, "Đã tạo trạng thái ban đầu:\n")
            self.log_text.insert(tk.END, format_floor(self.floor) + "\n")

        self.step_label.config(text="Step: 0")
        self.total_steps_label.config(text="Total steps: 0")
        self.time_label.config(text="Time: 0s")

    def solve_problem(self):
        
        algorithm = self.algorithm_var.get()

        if algorithm in ["Map Coloring Backtracking", "Forward Checking"]:
            self.open_map_coloring_window(algorithm)
            return

        if self.floor is None:
            messagebox.showwarning(
                "Thông báo",
                "Bạn cần bấm Random State trước."
            )
            return

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
            if self.is_no_observation_algorithm():
                self.prepare_belief_initial_state()
                result = solve(copy.deepcopy(self.belief_initial_state), algorithm)
            elif self.is_partial_observation_algorithm():
                if len(self.observed_positions) == 0:
                    messagebox.showwarning(
                        "Thông báo",
                        "Bạn cần Ctrl + Click chọn ít nhất 1 ô được nhìn thấy trước khi Solve."
                    )
                    return

                if self.belief_initial_state is None:
                    self.prepare_partial_belief_initial_state()
                    self.draw_belief_grid(self.result_grid_frame, self.belief_initial_state, small=True)

                partial_input = {
                    "actual_state": copy.deepcopy(self.floor),
                    "observed_positions": sorted(list(self.observed_positions)),
                    "initial_belief_state": copy.deepcopy(self.belief_initial_state)
                }
                result = solve(partial_input, algorithm)
            else:
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

        if self.is_belief_algorithm():
            self.handle_belief_result(result, log_algorithm_name)
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

    # =========================
    # XỬ LÝ KẾT QUẢ CHO BELIEF SEARCH
    # =========================
    def handle_belief_result(self, result, log_algorithm_name):
        self.solution_steps = result["path"]
        self.belief_actions = result.get("actions", [])
        self.current_step = -1
        self.is_running = True

        if self.is_no_observation_algorithm():
            self.draw_belief_grid(self.solve_grid_frame, self.solution_steps[0])
        elif self.is_partial_observation_algorithm():
            self.draw_observable_grid(self.solve_grid_frame, self.floor)

        self.draw_belief_grid(self.result_grid_frame, self.solution_steps[0], small=True)

        self.total_steps_label.config(
            text=f"Total steps: {len(self.solution_steps) - 1}"
        )
        self.time_label.config(
            text=f"Time: {self.execution_time:.6f}s"
        )

        final_belief_state = self.solution_steps[-1]

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
            "\nBelief state kết quả:\n" + self.format_belief_state(final_belief_state) + "\n"
        )

        self.auto_run_belief_steps()

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

    # =========================
    # AUTO RUN CHO BELIEF_STATE
    # =========================
    def auto_run_belief_steps(self):
        if not self.is_running:
            return

        if self.current_step < len(self.solution_steps) - 1:
            self.current_step += 1
            current_belief_state = self.solution_steps[self.current_step]

            self.draw_belief_grid(self.result_grid_frame, current_belief_state, small=True)
            self.step_label.config(text=f"Step: {self.current_step}")

            g_value = count_wrong_cells_in_belief(current_belief_state)
            h_value = manhattan_distance_in_belief(current_belief_state)
            f_value = g_value + h_value

            if self.current_step == 0:
                action_text = "Start"
            else:
                action_text = self.belief_actions[self.current_step - 1]

            self.log_text.insert(
                tk.END,
                f"---\nBelief State {self.current_step}:\n"
            )
            self.log_text.insert(
                tk.END,
                f"Action: {action_text}\n"
            )
            self.log_text.insert(
                tk.END,
                f"g(n)={g_value}, h(n)={h_value}, f(n)={f_value}\n"
            )
            self.log_text.insert(
                tk.END,
                self.format_belief_state(current_belief_state) + "\n"
            )
            self.log_text.see(tk.END)

            self.root.after(self.speed, self.auto_run_belief_steps)
        else:
            self.is_running = False
            self.log_text.insert(
                tk.END,
                "---\nĐã hoàn thành quá trình tìm kiếm belief_state.\n"
            )
            self.log_text.see(tk.END)
            messagebox.showinfo(
                "Hoàn thành",
                "Tất cả belief states đã hút sạch toàn bộ ô bẩn."
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
        self.belief_initial_state = None
        self.belief_actions = []
        self.observed_positions = set()

        self.draw_grid(self.solve_grid_frame, None)
        self.draw_grid(self.result_grid_frame, None)

        self.log_text.delete(1.0, tk.END)

        self.step_label.config(text="Step: 0")
        self.total_steps_label.config(text="Total steps: 0")
        self.time_label.config(text="Time: 0s")

    def on_speed_change(self, value):
        # Kéo sang phải thì chạy nhanh hơn
        self.speed = int(float(value))
