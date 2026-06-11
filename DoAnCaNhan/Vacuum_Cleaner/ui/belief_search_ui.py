import copy
import pygame

from algorithms.no_observation_search import (
    noobservationastar,
    belief_goal,
    count_wrong_cells_in_belief,
    manhattan_distance_in_belief
)


# =========================
# CẤU HÌNH GIAO DIỆN
# =========================
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
GRAY = (220, 220, 220)
DARK_GRAY = (80, 80, 80)
ORANGE = (255, 165, 0)
LIGHT_YELLOW = (249, 231, 159)


# =========================
# BELIEF SEARCH UI
# =========================
# Ý tưởng:
# - Giao diện riêng cho các thuật toán tìm kiếm trong môi trường phức tạp
# - Mỗi bước hiển thị belief_state
# - belief_state gồm nhiều trạng thái có thể xảy ra
# - Với bài hiện tại: hiển thị 2 ma trận cùng xử lý song song
# - ESC để thoát, R để chạy lại từ đầu
# =========================
class BeliefSearchUI:
    def __init__(self, initial_floor, algorithm_name="NoObservationSearch", step_delay=1000):
        self.initial_floor = copy.deepcopy(initial_floor)
        self.algorithm_name = algorithm_name
        self.step_delay = step_delay

        self.result = None
        self.belief_steps = []
        self.actions = []
        self.current_step = 0
        self.is_running = False
        self.last_step_time = 0

        self.screen = None
        self.clock = None
        self.font = None
        self.small_font = None
        self.title_font = None

        self.cell_size = 70
        self.padding = 24
        self.title_height = 115
        self.window_width = 900
        self.window_height = 520

        self.solve_algorithm()
        self.setup_pygame()

    # =========================
    # GỌI THUẬT TOÁN
    # =========================
    def solve_algorithm(self):
        if self.algorithm_name == "NoObservationSearch" or self.algorithm_name == "No Observation A*":
            self.result = noobservationastar(copy.deepcopy(self.initial_floor))
        else:
            self.result = noobservationastar(copy.deepcopy(self.initial_floor))

        if self.result is None:
            self.belief_steps = []
            self.actions = []
            return

        self.belief_steps = self.result["path"]
        self.actions = self.result.get("actions", [])

    # =========================
    # SETUP PYGAME
    # =========================
    def setup_pygame(self):
        pygame.init()

        rows, cols, state_count = self.get_grid_info()

        if state_count <= 2:
            self.cell_size = 70
        elif state_count <= 4:
            self.cell_size = 52
        else:
            self.cell_size = 38

        matrix_width = cols * self.cell_size
        matrix_height = rows * self.cell_size

        states_per_row = min(state_count, 4)
        total_rows = (state_count + states_per_row - 1) // states_per_row

        self.window_width = max(
            900,
            states_per_row * matrix_width + (states_per_row + 1) * self.padding
        )
        self.window_height = max(
            520,
            self.title_height + total_rows * (matrix_height + 55) + self.padding + 60
        )

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Belief Search Visualization")

        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 28, bold=True)
        self.clock = pygame.time.Clock()

    # =========================
    # LẤY THÔNG TIN KÍCH THƯỚC MA TRẬN
    # =========================
    def get_grid_info(self):
        if len(self.belief_steps) == 0:
            rows = len(self.initial_floor)
            cols = len(self.initial_floor[0])
            state_count = 1
            return rows, cols, state_count

        belief_state = self.belief_steps[0]
        state_count = len(belief_state)
        rows = len(belief_state[0])
        cols = len(belief_state[0][0])

        return rows, cols, state_count

    # =========================
    # VẼ 1 MA TRẬN STATE
    # =========================
    def draw_state(self, state, offset_x, offset_y, index):
        rows = len(state)
        cols = len(state[0])

        matrix_width = cols * self.cell_size
        matrix_height = rows * self.cell_size

        is_goal_state = True
        for row in state:
            for cell in row:
                if cell == 1:
                    is_goal_state = False
                    break
            if not is_goal_state:
                break

        border_color = ORANGE if is_goal_state else BLACK
        pygame.draw.rect(
            self.screen,
            border_color,
            (offset_x - 3, offset_y - 3, matrix_width + 6, matrix_height + 6),
            4
        )

        label_text = self.small_font.render(f"State {index + 1}", True, BLACK)
        label_rect = label_text.get_rect(center=(offset_x + matrix_width // 2, offset_y - 18))
        self.screen.blit(label_text, label_rect)

        for i in range(rows):
            for j in range(cols):
                x = offset_x + j * self.cell_size
                y = offset_y + i * self.cell_size
                value = state[i][j]

                if value == "V":
                    color = BLUE
                    text_value = "V"
                    text_color = WHITE
                elif value == 1:
                    color = RED
                    text_value = "1"
                    text_color = WHITE
                else:
                    color = GREEN
                    text_value = "0"
                    text_color = WHITE

                pygame.draw.rect(
                    self.screen,
                    color,
                    (x, y, self.cell_size, self.cell_size)
                )
                pygame.draw.rect(
                    self.screen,
                    BLACK,
                    (x, y, self.cell_size, self.cell_size),
                    2
                )

                cell_text = self.font.render(text_value, True, text_color)
                cell_rect = cell_text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                self.screen.blit(cell_text, cell_rect)

    # =========================
    # VẼ TOÀN BỘ BELIEF_STATE
    # =========================
    def draw_belief_state(self):
        self.screen.fill(WHITE)

        if len(self.belief_steps) == 0:
            title = "Không tìm thấy lời giải cho belief_state"
            title_surface = self.title_font.render(title, True, RED)
            title_rect = title_surface.get_rect(center=(self.window_width // 2, 45))
            self.screen.blit(title_surface, title_rect)
            pygame.display.flip()
            return

        belief_state = self.belief_steps[self.current_step]

        if self.current_step == 0:
            title = "Initial Belief States (ESC to quit, R to restart)"
        else:
            title = f"Step {self.current_step} (Algorithm: {self.algorithm_name}, ESC to quit, R to restart)"

        title_surface = self.title_font.render(title, True, BLACK)
        title_rect = title_surface.get_rect(center=(self.window_width // 2, 35))
        self.screen.blit(title_surface, title_rect)

        action_text = "Action: Start"
        if self.current_step > 0 and self.current_step - 1 < len(self.actions):
            action_text = f"Action: {self.actions[self.current_step - 1]}"

        action_surface = self.small_font.render(action_text, True, DARK_GRAY)
        action_rect = action_surface.get_rect(center=(self.window_width // 2, 68))
        self.screen.blit(action_surface, action_rect)

        g_value = count_wrong_cells_in_belief(belief_state)
        h_value = manhattan_distance_in_belief(belief_state)
        f_value = g_value + h_value

        info_text = f"g(n) = {g_value}    h(n) = {h_value}    f(n) = {f_value}    Total steps: {len(self.belief_steps) - 1}"
        info_surface = self.small_font.render(info_text, True, DARK_GRAY)
        info_rect = info_surface.get_rect(center=(self.window_width // 2, 94))
        self.screen.blit(info_surface, info_rect)

        rows = len(belief_state[0])
        cols = len(belief_state[0][0])
        state_count = len(belief_state)
        matrix_width = cols * self.cell_size
        matrix_height = rows * self.cell_size
        states_per_row = min(state_count, 4)

        start_y = self.title_height + 35

        for idx, state in enumerate(belief_state):
            row_index = idx // states_per_row
            col_index = idx % states_per_row

            total_width = states_per_row * matrix_width + (states_per_row - 1) * self.padding
            start_x = (self.window_width - total_width) // 2

            offset_x = start_x + col_index * (matrix_width + self.padding)
            offset_y = start_y + row_index * (matrix_height + 60)

            self.draw_state(state, offset_x, offset_y, idx)

        note = "0 = sạch, 1 = bẩn, V = máy hút bụi | Goal khi tất cả belief states đều sạch bụi"
        note_surface = self.small_font.render(note, True, DARK_GRAY)
        note_rect = note_surface.get_rect(center=(self.window_width // 2, self.window_height - 30))
        self.screen.blit(note_surface, note_rect)

        pygame.display.flip()

    # =========================
    # CHẠY TỪ ĐẦU
    # =========================
    def reset(self):
        self.current_step = 0
        self.is_running = True
        self.last_step_time = pygame.time.get_ticks()
        self.solve_algorithm()
        self.draw_belief_state()

    # =========================
    # VÒNG LẶP CHẠY UI
    # =========================
    def run(self):
        running = True
        self.is_running = True
        self.current_step = 0
        self.last_step_time = pygame.time.get_ticks()

        self.draw_belief_state()

        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.reset()

            if self.is_running and len(self.belief_steps) > 0:
                if current_time - self.last_step_time >= self.step_delay:
                    if self.current_step < len(self.belief_steps) - 1:
                        self.current_step += 1
                        self.last_step_time = current_time
                        self.draw_belief_state()
                    else:
                        self.is_running = False

                        final_belief_state = self.belief_steps[self.current_step]
                        if belief_goal(final_belief_state):
                            pygame.display.set_caption("Belief Search Visualization - Goal Reached")

            self.clock.tick(FPS)

        pygame.quit()


# =========================
# HÀM GỌI NHANH TỪ UI CHÍNH
# =========================
def run_belief_search_ui(initial_floor, algorithm_name="NoObservationSearch", step_delay=1000):
    belief_ui = BeliefSearchUI(
        initial_floor=initial_floor,
        algorithm_name=algorithm_name,
        step_delay=step_delay
    )
    belief_ui.run()
