import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import time

from PIL import Image, ImageTk, ImageDraw

from algorithms.backtracking import (
    mapcoloringbacktracking,
    REGIONS,
    COLORS
)

from algorithms.forward_checking import forwardchecking


# =========================
# UI CHUNG CHO MAP COLORING CSP
# =========================
# Dùng chung cho:
# - Map Coloring Backtracking
# - Forward Checking
#
# Luồng:
# - Chọn thuật toán trong Vacuum UI thì cửa sổ này hiện ngay
# - Cửa sổ chưa chạy ngay
# - Bấm Solve thì chạy đúng thuật toán đã chọn
# - Chạy xong giữ nguyên màn hình để quan sát
# =========================
class MapColoringUI:
    def __init__(self, root, algorithm_name="Map Coloring Backtracking"):
        self.root = root
        self.algorithm_name = algorithm_name

        self.root.title(self.algorithm_name)
        self.root.geometry("1380x780")
        self.root.minsize(1150, 700)
        self.root.resizable(True, True)

        self.result = None
        self.steps = []
        self.current_step = -1
        self.is_running = False
        self.speed = 650
        self.execution_time = 0

        self.color_map = {
            "Đỏ": (231, 76, 60),
            "Vàng": (241, 196, 15),
            "Xanh lá": (46, 204, 113),
            "Xanh dương": (52, 152, 219)
        }

        # Seed nằm trong vùng bản đồ, không nằm trong ô tròn số
        self.region_seeds = {
            1: (350, 150),
            2: (700, 140),
            3: (380, 500),
            4: (990, 160),
            5: (700, 470),
            6: (600, 625),
            7: (880, 685),
            8: (1110, 375),
            9: (1060, 600),
            10: (830, 860),
            11: (1180, 900)
        }

        self.original_image = None
        self.tk_image = None

        self.setup_styles()
        self.setup_ui()
        self.load_map_image()
        self.reset_screen()

    # =========================
    # ĐỔI THUẬT TOÁN TRÊN CÙNG 1 CỬA SỔ
    # =========================
    def set_algorithm(self, algorithm_name):
        self.algorithm_name = algorithm_name
        self.root.title(self.algorithm_name)
        self.title_label.config(text=self.algorithm_name)
        self.reset_screen()

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
            font=("Helvetica", 24, "bold"),
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
            "Large.TButton",
            font=("Helvetica", 12, "bold"),
            padding=8
        )

    # =========================
    # SETUP UI
    # =========================
    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, style="Content.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.title_label = ttk.Label(
            self.main_frame,
            text=self.algorithm_name,
            style="Title.TLabel"
        )
        self.title_label.pack(pady=(5, 4))

        self.info_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.info_frame.pack(pady=5)

        self.step_label = ttk.Label(
            self.info_frame,
            text="Step: 0",
            font=("Helvetica", 13, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.step_label.pack(side="left", padx=18)

        self.total_steps_label = ttk.Label(
            self.info_frame,
            text="Total steps: 0",
            font=("Helvetica", 13, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.total_steps_label.pack(side="left", padx=18)

        self.time_label = ttk.Label(
            self.info_frame,
            text="Time: 0s",
            font=("Helvetica", 13, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.time_label.pack(side="left", padx=18)

        self.status_label = ttk.Label(
            self.info_frame,
            text="Status: Ready",
            font=("Helvetica", 13, "bold"),
            background="#ECF0F1",
            foreground="#34495E"
        )
        self.status_label.pack(side="left", padx=18)

        self.body_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.body_frame.pack(fill="both", expand=True, pady=10)

        self.body_frame.columnconfigure(0, weight=5, minsize=650)
        self.body_frame.columnconfigure(1, weight=4, minsize=520)
        self.body_frame.rowconfigure(0, weight=1)

        # LEFT PANEL
        self.left_panel = tk.Frame(
            self.body_frame,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ttk.Label(
            self.left_panel,
            text="Bản đồ tô màu",
            style="PanelTitle.TLabel"
        ).pack(pady=(8, 4))

        self.canvas = tk.Canvas(
            self.left_panel,
            bg="#FFFFFF",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)

        # RIGHT PANEL
        self.right_panel = tk.Frame(
            self.body_frame,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        ttk.Label(
            self.right_panel,
            text="Process Log",
            style="PanelTitle.TLabel"
        ).pack(pady=(8, 4))

        self.log_inner = tk.Frame(self.right_panel, bg="#FFFFFF")
        self.log_inner.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.log_scrollbar = ttk.Scrollbar(self.log_inner, orient=tk.VERTICAL)

        self.log_text = tk.Text(
            self.log_inner,
            height=24,
            width=58,
            font=("Consolas", 10),
            bg="#F9E79F",
            yscrollcommand=self.log_scrollbar.set,
            relief="flat",
            borderwidth=1
        )

        self.log_scrollbar.config(command=self.log_text.yview)
        self.log_scrollbar.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

        # DOMAIN PANEL
        ttk.Label(
            self.right_panel,
            text="Domain hiện tại",
            style="PanelTitle.TLabel"
        ).pack(pady=(2, 4))

        self.domain_text = tk.Text(
            self.right_panel,
            height=8,
            width=58,
            font=("Consolas", 10),
            bg="#EAF2F8",
            relief="flat",
            borderwidth=1
        )
        self.domain_text.pack(fill="x", padx=10, pady=(0, 10))

        # BUTTONS
        self.button_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.button_frame.pack(fill="x", pady=(0, 5))

        ttk.Button(
            self.button_frame,
            text="Solve",
            command=self.solve_algorithm,
            style="Large.TButton"
        ).pack(side="left", padx=8)

        ttk.Button(
            self.button_frame,
            text="Restart",
            command=self.solve_algorithm,
            style="Large.TButton"
        ).pack(side="left", padx=8)

        ttk.Button(
            self.button_frame,
            text="Stop",
            command=self.stop,
            style="Large.TButton"
        ).pack(side="left", padx=8)

        ttk.Label(
            self.button_frame,
            text="Tốc độ:",
            background="#ECF0F1",
            font=("Helvetica", 11, "bold")
        ).pack(side="left", padx=(30, 5))

        self.speed_scale = ttk.Scale(
            self.button_frame,
            from_=1500,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.on_speed_change
        )
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side="left", padx=5, fill="x", expand=True)

    # =========================
    # TÌM FILE ẢNH MAP
    # =========================
    def find_map_path(self):
        current_file = Path(__file__).resolve()

        candidates = [
            current_file.parent.parent / "assets" / "map_tphcm.png",
            current_file.parent / "assets" / "map_tphcm.png",
            Path.cwd() / "assets" / "map_tphcm.png",
            Path.cwd() / "map_tphcm.png"
        ]

        for path in candidates:
            if path.exists():
                return path

        return None

    # =========================
    # LOAD ẢNH MAP
    # =========================
    def load_map_image(self):
        map_path = self.find_map_path()

        if map_path is None:
            messagebox.showerror(
                "Thiếu ảnh bản đồ",
                "Không tìm thấy file assets/map_tphcm.png.\nBạn hãy đặt ảnh bản đồ vào thư mục assets."
            )
            return

        self.original_image = Image.open(map_path).convert("RGB")

    # =========================
    # RESET MÀN HÌNH
    # =========================
    def reset_screen(self):
        self.is_running = False
        self.result = None
        self.steps = []
        self.current_step = -1
        self.execution_time = 0

        self.step_label.config(text="Step: 0")
        self.total_steps_label.config(text="Total steps: 0")
        self.time_label.config(text="Time: 0s")
        self.status_label.config(text="Status: Ready")

        self.log_text.delete(1.0, tk.END)
        self.domain_text.delete(1.0, tk.END)

        self.log_text.insert(
            tk.END,
            f"Đã chọn thuật toán: {self.algorithm_name}\n"
        )
        self.log_text.insert(
            tk.END,
            "Bấm Solve để bắt đầu mô phỏng.\n"
        )

        if self.algorithm_name == "Forward Checking":
            self.log_text.insert(
                tk.END,
                "Forward Checking sẽ hiển thị thêm domain hiện tại.\n"
            )
        else:
            self.log_text.insert(
                tk.END,
                "Backtracking thường chỉ thử màu và quay lui khi bị kẹt.\n"
            )

        self.draw_map({})

    # =========================
    # TÔ MÀU MAP BẰNG FLOOD FILL
    # =========================
    def build_colored_map(self, assignment, current_region=None, current_color=None, step_type=None):
        if self.original_image is None:
            return None

        img = self.original_image.copy()

        for region in assignment:
            color_name = assignment[region]
            fill_color = self.color_map[color_name]
            seed = self.region_seeds[region]

            ImageDraw.floodfill(
                img,
                seed,
                fill_color,
                thresh=50
            )

        if step_type == "try" and current_region is not None and current_color is not None:
            temp_color = self.color_map[current_color]
            seed = self.region_seeds[current_region]

            ImageDraw.floodfill(
                img,
                seed,
                temp_color,
                thresh=50
            )

        return img

    # =========================
    # VẼ MAP
    # =========================
    def draw_map(self, assignment, current_region=None, current_color=None, step_type=None):
        img = self.build_colored_map(
            assignment,
            current_region=current_region,
            current_color=current_color,
            step_type=step_type
        )

        if img is None:
            return

        canvas_width = max(500, self.canvas.winfo_width())
        canvas_height = max(400, self.canvas.winfo_height())

        img_w, img_h = img.size
        scale = min(
            canvas_width / img_w,
            canvas_height / img_h
        )

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        img = img.resize((new_w, new_h), Image.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.tk_image,
            anchor="center"
        )

        legend_x = 20
        legend_y = 20

        self.canvas.create_text(
            legend_x,
            legend_y,
            text="Màu:",
            anchor="w",
            font=("Helvetica", 11, "bold")
        )

        offset = 65

        for color_name in COLORS:
            rgb = self.color_map[color_name]
            hex_color = "#%02x%02x%02x" % rgb
            x = legend_x + offset

            self.canvas.create_rectangle(
                x,
                legend_y - 10,
                x + 18,
                legend_y + 8,
                fill=hex_color,
                outline="#000000"
            )

            self.canvas.create_text(
                x + 24,
                legend_y,
                text=color_name,
                anchor="w",
                font=("Helvetica", 10)
            )

            offset += 115

    # =========================
    # GỌI ĐÚNG THUẬT TOÁN
    # =========================
    def run_selected_algorithm(self):
        if self.algorithm_name == "Forward Checking":
            return forwardchecking()

        return mapcoloringbacktracking()

    # =========================
    # SOLVE
    # =========================
    def solve_algorithm(self):
        self.is_running = False
        self.current_step = -1
        self.execution_time = 0

        self.log_text.delete(1.0, tk.END)
        self.domain_text.delete(1.0, tk.END)
        self.draw_map({})

        start_time = time.perf_counter()
        self.result = self.run_selected_algorithm()
        end_time = time.perf_counter()

        self.execution_time = end_time - start_time
        self.steps = self.result["steps"]

        self.total_steps_label.config(text=f"Total steps: {len(self.steps)}")
        self.time_label.config(text=f"Time: {self.execution_time:.6f}s")
        self.step_label.config(text="Step: 0")
        self.status_label.config(text="Status: Running")

        self.log_text.insert(tk.END, f"Bắt đầu mô phỏng {self.algorithm_name}.\n")
        self.log_text.insert(tk.END, "Miền giá trị: {Đỏ, Vàng, Xanh lá, Xanh dương}\n")
        self.log_text.insert(tk.END, "Ràng buộc: hai vùng kề nhau không được cùng màu.\n")

        if self.algorithm_name == "Forward Checking":
            self.log_text.insert(
                tk.END,
                "Cơ chế: sau khi gán màu, xóa màu đó khỏi domain của vùng kề chưa tô.\n"
            )
        else:
            self.log_text.insert(
                tk.END,
                "Cơ chế: thử màu, nếu nhánh sau thất bại thì quay lui.\n"
            )

        self.log_text.insert(
            tk.END,
            f"Thời gian thực thi thuật toán: {self.execution_time:.6f}s\n\n"
        )
        self.log_text.see(tk.END)

        self.is_running = True
        self.root.after(200, self.run_next_auto_step)

    # =========================
    # HIỂN THỊ DOMAIN
    # =========================
    def show_domains(self, domains):
        self.domain_text.delete(1.0, tk.END)

        if domains is None:
            self.domain_text.insert(
                tk.END,
                "Backtracking thường không lưu domain cắt giảm.\n"
            )
            return

        for region in sorted(domains.keys()):
            colors = ", ".join(domains[region])
            line = f"{REGIONS[region]}: {{{colors}}}\n"
            self.domain_text.insert(tk.END, line)

    # =========================
    # HIỂN THỊ 1 BƯỚC
    # =========================
    def show_current_step(self, step):
        assignment = step["assignment"]
        domains = step.get("domains")
        current_region = step["region"]
        current_color = step["color"]
        step_type = step["type"]
        removed_values = step.get("removed_values", [])

        self.draw_map(
            assignment,
            current_region=current_region,
            current_color=current_color,
            step_type=step_type
        )

        self.show_domains(domains)

        self.step_label.config(text=f"Step: {self.current_step + 1}")
        self.status_label.config(text=f"Status: {step_type}")

        self.log_text.insert(
            tk.END,
            f"---\nBước {self.current_step + 1}: {step['message']}\n"
        )

        if current_region is not None:
            self.log_text.insert(
                tk.END,
                f"Vùng đang xét: {REGIONS[current_region]}\n"
            )

        if current_color is not None:
            self.log_text.insert(
                tk.END,
                f"Màu đang thử/gán: {current_color}\n"
            )

        if len(removed_values) > 0:
            self.log_text.insert(tk.END, "Miền bị cắt:\n")

            for item in removed_values:
                neighbor = item[0]
                removed_color = item[1]
                self.log_text.insert(
                    tk.END,
                    f"  - Xóa {removed_color} khỏi domain của {REGIONS[neighbor]}\n"
                )

        self.log_text.insert(
            tk.END,
            f"Assignment hiện tại: {self.format_assignment(assignment)}\n"
        )

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

            self.log_text.insert(
                tk.END,
                "\n---\nĐã hoàn thành thuật toán.\n"
            )
            self.log_text.insert(
                tk.END,
            )
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
    # FORMAT ASSIGNMENT
    # =========================
    def format_assignment(self, assignment):
        if len(assignment) == 0:
            return "{}"

        parts = []

        for region in assignment:
            parts.append(f"{REGIONS[region]}={assignment[region]}")

        return "{ " + ", ".join(parts) + " }"

    # =========================
    # SPEED
    # =========================
    def on_speed_change(self, value):
        self.speed = int(float(value))


if __name__ == "__main__":
    root = tk.Tk()
    app = MapColoringUI(root, "Map Coloring Backtracking")
    root.mainloop()
