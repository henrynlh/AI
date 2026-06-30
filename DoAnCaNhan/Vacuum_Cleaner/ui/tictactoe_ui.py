import tkinter as tk
from tkinter import ttk, messagebox
import time

from algorithms.caro_game import (
    EMPTY,
    MAX_PLAYER,
    MIN_PLAYER,
    copy_board,
    create_demo_board,
    create_empty_board,
    format_board,
    format_move,
    get_current_player,
    get_winner,
    is_board_full,
    is_valid_game_board
)
from algorithms.minimax import minimax_search
from algorithms.alpha_beta import alphabeta_search
from algorithms.expectimax import expectimax_search
from algorithms.algorithm_manager import get_adversarial_algorithms


# =========================
# UI MÔ PHỎNG NHÓM THUẬT TOÁN ĐỐI KHÁNG
# =========================
# Dùng chung cho:
# - Minimax
# - Alpha-Beta Pruning
# - Expectimax
#
# Ý tưởng visualizer:
# - Bài toán minh họa là cờ ca rô 3x3.
# - Người dùng có thể click từng ô để tự tạo trạng thái ban đầu.
# - Bấm Solve để thuật toán phân tích cây trò chơi và chọn nước đi tốt nhất.
# - Mỗi step hiển thị board đang xét, node type, điểm, alpha/beta hoặc kỳ vọng.
# =========================
class TicTacToeUI:
    def __init__(self, root, algorithm_name="Minimax"):
        self.root = root
        self.algorithm_values = get_adversarial_algorithms()
        self.algorithm_name = algorithm_name
        if self.algorithm_name not in self.algorithm_values:
            self.algorithm_name = self.algorithm_values[0]

        self.root.title(self.algorithm_name + " - Cờ ca rô")
        self.root.geometry("1180x720")
        self.root.minsize(980, 640)
        self.root.resizable(True, True)

        self.board = create_demo_board()
        self.result = None
        self.steps = []
        self.current_step = -1
        self.is_running = False
        self.speed = 650
        self.execution_time = 0
        self.cell_buttons = []

        self.setup_styles()
        self.setup_ui()
        self.reset_screen()

    # =========================
    # ĐỔI THUẬT TOÁN TRÊN CÙNG 1 CỬA SỔ
    # =========================
    def set_algorithm(self, algorithm_name):
        if algorithm_name not in self.algorithm_values:
            algorithm_name = self.algorithm_values[0]

        self.algorithm_name = algorithm_name
        self.root.title(self.algorithm_name + " - Cờ ca rô")
        self.title_label.config(text="Đối kháng - Cờ ca rô")

        if hasattr(self, "algorithm_var"):
            self.algorithm_var.set(self.algorithm_name)

        self.reset_screen(keep_board=True)

    # =========================
    # ĐỔI THUẬT TOÁN TRONG CỬA SỔ CỜ CA RÔ
    # =========================
    def on_algorithm_change(self, event=None):
        self.set_algorithm(self.algorithm_var.get())

    # =========================
    # STYLE
    # =========================
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Content.TFrame", background="#ECF0F1")
        style.configure("Panel.TFrame", background="#ECF0F1")

        style.configure(
            "Title.TLabel",
            font=("Helvetica", 20, "bold"),
            background="#ECF0F1",
            foreground="#2C3E50"
        )

        style.configure(
            "PanelTitle.TLabel",
            font=("Helvetica", 13, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )

        style.configure(
            "Large.TButton",
            font=("Helvetica", 10, "bold"),
            padding=5
        )

    # =========================
    # SETUP UI
    # =========================
    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, style="Content.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Dùng grid cho layout tổng để thanh điều khiển phía dưới luôn còn chỗ hiển thị.
        # Chỉ vùng thân giữa được co giãn; title, thông tin và button bar giữ chiều cao cố định.
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=0)
        self.main_frame.rowconfigure(2, weight=0)
        self.main_frame.rowconfigure(3, weight=1)
        self.main_frame.rowconfigure(4, weight=0)

        self.title_label = ttk.Label(
            self.main_frame,
            text="Đối kháng - Cờ ca rô",
            style="Title.TLabel"
        )
        self.title_label.grid(row=0, column=0, pady=(0, 3), sticky="n")

        # Chọn thuật toán ngay trong visualizer đối kháng.
        # Luồng mô phỏng lúc này là: chọn nhóm Đối kháng ở màn hình chính ->
        # mở bàn cờ -> chọn Minimax / Alpha-Beta / Expectimax trong cửa sổ cờ.
        self.algorithm_select_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.algorithm_select_frame.grid(row=1, column=0, pady=(0, 4), sticky="n")

        ttk.Label(
            self.algorithm_select_frame,
            text="Thuật toán đối kháng:",
            background="#ECF0F1",
            font=("Helvetica", 11, "bold")
        ).pack(side="left", padx=(0, 8))

        self.algorithm_var = tk.StringVar(value=self.algorithm_name)
        self.algorithm_combobox = ttk.Combobox(
            self.algorithm_select_frame,
            textvariable=self.algorithm_var,
            values=self.algorithm_values,
            state="readonly",
            width=24,
            font=("Helvetica", 11)
        )
        self.algorithm_combobox.pack(side="left")
        self.algorithm_combobox.bind("<<ComboboxSelected>>", self.on_algorithm_change)

        self.info_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.info_frame.grid(row=2, column=0, pady=(0, 5), sticky="n")

        self.step_label = ttk.Label(
            self.info_frame,
            text="Step: 0",
            font=("Helvetica", 10, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.step_label.pack(side="left", padx=10)

        self.total_steps_label = ttk.Label(
            self.info_frame,
            text="Total steps: 0",
            font=("Helvetica", 10, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.total_steps_label.pack(side="left", padx=10)

        self.time_label = ttk.Label(
            self.info_frame,
            text="Time: 0s",
            font=("Helvetica", 10, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.time_label.pack(side="left", padx=10)

        self.status_label = ttk.Label(
            self.info_frame,
            text="Status: Ready",
            font=("Helvetica", 10, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.status_label.pack(side="left", padx=10)

        self.expanded_label = ttk.Label(
            self.info_frame,
            text="Expanded: 0",
            font=("Helvetica", 10, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.expanded_label.pack(side="left", padx=10)

        self.body_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.body_frame.grid(row=3, column=0, sticky="nsew", pady=(4, 6))

        self.body_frame.columnconfigure(0, weight=3, minsize=300)
        self.body_frame.columnconfigure(1, weight=4, minsize=380)
        self.body_frame.columnconfigure(2, weight=3, minsize=280)
        self.body_frame.rowconfigure(0, weight=1)

        # =========================
        # PANEL TRÁI: BÀN CỜ
        # =========================
        self.board_panel = tk.Frame(
            self.body_frame,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.board_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        ttk.Label(
            self.board_panel,
            text="Bàn cờ / trạng thái",
            style="PanelTitle.TLabel"
        ).pack(pady=(6, 2))

        self.turn_label = tk.Label(
            self.board_panel,
            text="Lượt đi: X",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#2C3E50"
        )
        self.turn_label.pack(pady=(0, 4))

        self.board_frame = tk.Frame(self.board_panel, bg="#FFFFFF")
        self.board_frame.pack(expand=True)

        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Helvetica", 26, "bold"),
                    bg="#FDFEFE",
                    fg="#2C3E50",
                    activebackground="#D6EAF8",
                    relief="solid",
                    bd=2,
                    command=lambda r=i, c=j: self.on_cell_click(r, c)
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
                row_buttons.append(btn)
            self.cell_buttons.append(row_buttons)

        self.best_move_label = tk.Label(
            self.board_panel,
            text="Best move: --",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#2C3E50"
        )
        self.best_move_label.pack(pady=(8, 2))

        self.help_label = tk.Label(
            self.board_panel,
            text="Click ô để đổi: trống → X → O → trống",
            font=("Helvetica", 9),
            bg="#FFFFFF",
            fg="#566573"
        )
        self.help_label.pack(pady=(2, 6))

        # =========================
        # PANEL GIỮA: LOG
        # =========================
        self.log_panel = tk.Frame(
            self.body_frame,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.log_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 6))

        ttk.Label(
            self.log_panel,
            text="Process Log",
            style="PanelTitle.TLabel"
        ).pack(pady=(6, 2))

        self.log_inner = tk.Frame(self.log_panel, bg="#FFFFFF")
        self.log_inner.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.log_scrollbar = ttk.Scrollbar(self.log_inner, orient=tk.VERTICAL)

        self.log_text = tk.Text(
            self.log_inner,
            height=18,
            width=46,
            font=("Consolas", 9),
            bg="#F9E79F",
            yscrollcommand=self.log_scrollbar.set,
            relief="flat",
            borderwidth=1
        )

        self.log_scrollbar.config(command=self.log_text.yview)
        self.log_scrollbar.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

        # =========================
        # PANEL PHẢI: ĐIỂM NƯỚC ĐI
        # =========================
        self.score_panel = tk.Frame(
            self.body_frame,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.score_panel.grid(row=0, column=2, sticky="nsew")

        ttk.Label(
            self.score_panel,
            text="Candidate scores",
            style="PanelTitle.TLabel"
        ).pack(pady=(6, 2))

        self.score_text = tk.Text(
            self.score_panel,
            height=13,
            width=32,
            font=("Consolas", 9),
            bg="#EAF2F8",
            relief="flat",
            borderwidth=1
        )
        self.score_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.note_text = tk.Text(
            self.score_panel,
            height=6,
            width=32,
            font=("Consolas", 9),
            bg="#F4F6F7",
            relief="flat",
            borderwidth=1
        )
        self.note_text.pack(fill="x", padx=8, pady=(0, 8))

        # =========================
        # BUTTON BAR
        # =========================
        self.button_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.button_frame.grid(row=4, column=0, sticky="ew", pady=(0, 0))
        self.button_frame.columnconfigure(10, weight=1)

        ttk.Button(
            self.button_frame,
            text="Solve",
            command=self.solve_algorithm,
            style="Large.TButton"
        ).pack(side="left", padx=4)

        ttk.Button(
            self.button_frame,
            text="Restart",
            command=self.solve_algorithm,
            style="Large.TButton"
        ).pack(side="left", padx=4)

        ttk.Button(
            self.button_frame,
            text="Stop",
            command=self.stop,
            style="Large.TButton"
        ).pack(side="left", padx=4)

        ttk.Button(
            self.button_frame,
            text="Demo",
            command=self.load_demo_board,
            style="Large.TButton"
        ).pack(side="left", padx=4)

        ttk.Button(
            self.button_frame,
            text="Clear",
            command=self.clear_board,
            style="Large.TButton"
        ).pack(side="left", padx=4)

        ttk.Label(
            self.button_frame,
            text="Depth:",
            background="#ECF0F1",
            font=("Helvetica", 10, "bold")
        ).pack(side="left", padx=(12, 4))

        self.depth_var = tk.StringVar(value="5")
        self.depth_combobox = ttk.Combobox(
            self.button_frame,
            textvariable=self.depth_var,
            values=["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            state="readonly",
            width=5,
            font=("Helvetica", 10)
        )
        self.depth_combobox.pack(side="left", padx=4)

        ttk.Label(
            self.button_frame,
            text="Speed:",
            background="#ECF0F1",
            font=("Helvetica", 10, "bold")
        ).pack(side="left", padx=(12, 4))

        self.speed_scale = ttk.Scale(
            self.button_frame,
            from_=1500,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.on_speed_change
        )
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side="left", padx=4, fill="x", expand=True)

    # =========================
    # CLICK Ô CỜ
    # =========================
    def on_cell_click(self, row, col):
        if self.is_running:
            return

        current = self.board[row][col]

        if current == EMPTY:
            self.board[row][col] = MAX_PLAYER
        elif current == MAX_PLAYER:
            self.board[row][col] = MIN_PLAYER
        else:
            self.board[row][col] = EMPTY

        self.reset_screen(keep_board=True)

    # =========================
    # RESET MÀN HÌNH
    # =========================
    def reset_screen(self, keep_board=True):
        self.is_running = False
        self.result = None
        self.steps = []
        self.current_step = -1
        self.execution_time = 0

        self.step_label.config(text="Step: 0")
        self.total_steps_label.config(text="Total steps: 0")
        self.time_label.config(text="Time: 0s")
        self.status_label.config(text="Status: Ready")
        self.expanded_label.config(text="Expanded: 0")
        self.best_move_label.config(text="Best move: --")

        self.log_text.delete(1.0, tk.END)
        self.score_text.delete(1.0, tk.END)
        self.note_text.delete(1.0, tk.END)

        self.log_text.insert(tk.END, "Đã chọn thuật toán: " + self.algorithm_name + "\n")
        self.log_text.insert(tk.END, "Bấm Solve để thuật toán chọn nước đi tốt nhất.\n")
        self.log_text.insert(tk.END, "Bạn có thể click vào bàn cờ để tự tạo trạng thái ban đầu.\n\n")

        if self.algorithm_name == "Minimax":
            self.log_text.insert(tk.END, "Cơ chế: MAX chọn max, MIN chọn min.\n")
        elif self.algorithm_name == "Alpha-Beta Pruning":
            self.log_text.insert(tk.END, "Cơ chế: Minimax + cắt tỉa khi alpha >= beta.\n")
        else:
            self.log_text.insert(tk.END, "Cơ chế: MAX chọn max, O là CHANCE node lấy điểm kỳ vọng.\n")

        self.show_algorithm_note()
        self.draw_board(self.board)

    # =========================
    # GHI CHÚ GIẢI THÍCH THUẬT TOÁN
    # =========================
    def show_algorithm_note(self):
        self.note_text.delete(1.0, tk.END)

        if self.algorithm_name == "Minimax":
            text = (
                "MINIMAX\n"
                "- X là MAX.\n"
                "- O là MIN.\n"
                "- MAX chọn điểm lớn nhất.\n"
                "- MIN chọn điểm nhỏ nhất.\n"
                "- Giả định đối thủ chơi tối ưu.\n"
            )
        elif self.algorithm_name == "Alpha-Beta Pruning":
            text = (
                "ALPHA-BETA\n"
                "- Kết quả như Minimax.\n"
                "- alpha: cận tốt nhất của MAX.\n"
                "- beta: cận tốt nhất của MIN.\n"
                "- alpha >= beta thì cắt nhánh.\n"
            )
        else:
            text = (
                "EXPECTIMAX\n"
                "- X là MAX.\n"
                "- O là CHANCE node.\n"
                "- Mỗi nước O có xác suất đều.\n"
                "- Chọn nước có expected score lớn nhất.\n"
            )

        self.note_text.insert(tk.END, text)

    # =========================
    # VẼ BÀN CỜ
    # =========================
    def draw_board(self, board, highlight_move=None, step_type=None):
        for i in range(3):
            for j in range(3):
                value = board[i][j]
                btn = self.cell_buttons[i][j]

                if value == EMPTY:
                    text = ""
                    fg = "#2C3E50"
                else:
                    text = value
                    if value == MAX_PLAYER:
                        fg = "#E74C3C"
                    else:
                        fg = "#2980B9"

                bg = "#FDFEFE"

                if highlight_move == (i, j):
                    if step_type == "prune":
                        bg = "#F5B7B1"
                    elif step_type == "done":
                        bg = "#ABEBC6"
                    else:
                        bg = "#F9E79F"

                btn.config(text=text, fg=fg, bg=bg)

        winner = get_winner(board)

        if winner is not None:
            turn_text = "Kết quả: " + winner + " thắng"
        elif is_board_full(board):
            turn_text = "Kết quả: Hòa"
        else:
            turn_text = "Lượt đi tiếp: " + get_current_player(board)

        self.turn_label.config(text=turn_text)

    # =========================
    # HIỂN THỊ ĐIỂM CÁC NƯỚC ĐI
    # =========================
    def show_candidate_scores(self, candidate_scores):
        self.score_text.delete(1.0, tk.END)

        if len(candidate_scores) == 0:
            self.score_text.insert(tk.END, "Chưa có danh sách điểm nước đi.\n")
            return

        self.score_text.insert(tk.END, "Move       Score        Ghi chú\n")
        self.score_text.insert(tk.END, "--------------------------------\n")

        for item in candidate_scores:
            move = format_move(item.get("move"))
            score = str(item.get("score"))
            note = item.get("note", "")

            if "probability" in item:
                note = "p=" + str(item.get("probability")) + " " + note

            line = move.ljust(10) + score.ljust(13) + note + "\n"
            self.score_text.insert(tk.END, line)

    # =========================
    # KIỂM TRA BOARD TRƯỚC KHI SOLVE
    # =========================
    def validate_board_before_solve(self):
        if not is_valid_game_board(self.board):
            messagebox.showwarning(
                "Bàn cờ không hợp lệ",
                "Trạng thái bàn cờ chưa hợp lệ. X đi trước; số quân X/O phải đúng lượt và không được có hai bên cùng thắng."
            )
            return False

        if get_current_player(self.board) != MAX_PLAYER:
            messagebox.showwarning(
                "Chưa đến lượt X",
                "Visualizer này mô phỏng thuật toán chọn nước đi cho X. Hãy tạo trạng thái có số quân X bằng số quân O để X đi tiếp."
            )
            return False

        return True

    # =========================
    # GỌI ĐÚNG THUẬT TOÁN
    # =========================
    def run_selected_algorithm(self):
        max_depth = int(self.depth_var.get())
        board = copy_board(self.board)

        if self.algorithm_name == "Alpha-Beta Pruning":
            return alphabeta_search(board=board, max_depth=max_depth)

        if self.algorithm_name == "Expectimax":
            return expectimax_search(board=board, max_depth=max_depth)

        return minimax_search(board=board, max_depth=max_depth)

    # =========================
    # SOLVE
    # =========================
    def solve_algorithm(self):
        if not self.validate_board_before_solve():
            return

        self.is_running = False
        self.current_step = -1
        self.execution_time = 0

        self.log_text.delete(1.0, tk.END)
        self.score_text.delete(1.0, tk.END)
        self.draw_board(self.board)

        start_time = time.perf_counter()
        self.result = self.run_selected_algorithm()
        end_time = time.perf_counter()

        self.execution_time = end_time - start_time
        self.steps = self.result["steps"]

        self.total_steps_label.config(text="Total steps: " + str(len(self.steps)))
        self.time_label.config(text="Time: " + f"{self.execution_time:.6f}" + "s")
        self.step_label.config(text="Step: 0")
        self.status_label.config(text="Status: Running")
        self.expanded_label.config(text="Expanded: " + str(self.result["expanded_nodes"]))
        self.best_move_label.config(
            text="Best move: " + format_move(self.result["best_move"]) +
                 " | Score: " + str(self.result["best_score"])
        )

        self.log_text.insert(tk.END, "Bắt đầu mô phỏng " + self.algorithm_name + ".\n")
        self.log_text.insert(tk.END, "Board ban đầu:\n" + format_board(self.board) + "\n")
        self.log_text.insert(tk.END, "Depth limit: " + self.depth_var.get() + "\n")
        self.log_text.insert(tk.END, "Thời gian thực thi thuật toán: " + f"{self.execution_time:.6f}" + "s\n")
        self.log_text.insert(tk.END, "Expanded nodes: " + str(self.result["expanded_nodes"]) + "\n")
        self.log_text.insert(tk.END, "Best move: " + format_move(self.result["best_move"]) + "\n\n")
        self.log_text.see(tk.END)

        self.is_running = True
        self.root.after(200, self.run_next_auto_step)

    # =========================
    # HIỂN THỊ 1 BƯỚC
    # =========================
    def show_current_step(self, step):
        board = step["board"]
        move = step.get("move")
        step_type = step.get("type")
        candidate_scores = step.get("candidate_scores", [])
        manual_log = step.get("manual_log", [])

        self.draw_board(board, highlight_move=move, step_type=step_type)
        self.show_candidate_scores(candidate_scores)

        self.step_label.config(text="Step: " + str(self.current_step + 1))
        self.status_label.config(text="Status: " + step_type)

        self.log_text.insert(tk.END, "---\n")
        self.log_text.insert(tk.END, "Bước " + str(self.current_step + 1) + ": " + step["message"] + "\n")
        self.log_text.insert(tk.END, "Node type: " + str(step.get("node_type")) + "\n")
        self.log_text.insert(tk.END, "Depth: " + str(step.get("depth")) + "\n")

        if step.get("score") is not None:
            self.log_text.insert(tk.END, "Score: " + str(step.get("score")) + "\n")

        if step.get("alpha") is not None or step.get("beta") is not None:
            self.log_text.insert(tk.END, "alpha = " + str(step.get("alpha")) + ", beta = " + str(step.get("beta")) + "\n")

        if step.get("probability") is not None:
            self.log_text.insert(tk.END, "p = " + str(round(step.get("probability"), 3)) + "\n")

        if step.get("pruned"):
            self.log_text.insert(tk.END, "=> Có cắt tỉa nhánh tại bước này.\n")

        if len(manual_log) > 0:
            for line in manual_log:
                self.log_text.insert(tk.END, line + "\n")

        self.log_text.see(tk.END)

    # =========================
    # AUTO RUN
    # =========================
    def run_next_auto_step(self):
        if not self.is_running:
            return

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            step = self.steps[self.current_step]
            self.show_current_step(step)
            self.root.after(self.speed, self.run_next_auto_step)

        else:
            self.is_running = False
            self.status_label.config(text="Status: Finished")

            if self.result is not None:
                self.draw_board(
                    self.result["final_board"],
                    highlight_move=self.result["best_move"],
                    step_type="done"
                )

            self.log_text.insert(tk.END, "\n---\nĐã hoàn thành thuật toán.\n")
            self.log_text.see(tk.END)

    # =========================
    # STOP
    # =========================
    def stop(self):
        self.is_running = False
        self.status_label.config(text="Status: Stopped")
        self.log_text.insert(tk.END, "\nĐã dừng bởi người dùng.\n")
        self.log_text.see(tk.END)

    # =========================
    # LOAD DEMO / CLEAR
    # =========================
    def load_demo_board(self):
        if self.is_running:
            return

        self.board = create_demo_board()
        self.reset_screen(keep_board=True)

    def clear_board(self):
        if self.is_running:
            return

        self.board = create_empty_board()
        self.reset_screen(keep_board=True)

    # =========================
    # SPEED
    # =========================
    def on_speed_change(self, value):
        self.speed = int(float(value))


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeUI(root, "Alpha-Beta Pruning")
    root.mainloop()
