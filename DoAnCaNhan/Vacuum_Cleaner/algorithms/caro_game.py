# =========================
# CARO / TIC-TAC-TOE GAME UTILS
# =========================
# File này chứa các hàm dùng chung cho nhóm thuật toán đối kháng:
# - Minimax
# - Alpha-Beta Pruning
# - Expectimax
#
# Trong đồ án cá nhân, để mô phỏng rõ cây trò chơi và tránh không gian trạng thái
# quá lớn của caro 5 quân thắng, visualizer dùng bàn cờ caro 3x3.
# Cách này tương đương Tic-Tac-Toe, rất phù hợp để minh họa thuật toán đối kháng.
# =========================


# =========================
# KÝ HIỆU TRÊN BÀN CỜ
# =========================
EMPTY = ""
MAX_PLAYER = "X"   # Người chơi MAX: thuật toán cần chọn nước đi tốt nhất
MIN_PLAYER = "O"   # Người chơi MIN / đối thủ

BOARD_SIZE = 3
WIN_LENGTH = 3


# =========================
# TẠO BÀN CỜ RỖNG
# =========================
def create_empty_board():
    board = []

    for i in range(BOARD_SIZE):
        row = []
        for j in range(BOARD_SIZE):
            row.append(EMPTY)
        board.append(row)

    return board


# =========================
# BÀN CỜ MẪU CHO UI
# =========================
# Ý tưởng:
# - Không để bàn cờ quá rỗng vì cây tìm kiếm sẽ dài và khó quan sát.
# - Không để trạng thái quá dễ thắng ngay để log vẫn có nhiều nhánh cần so sánh.
# =========================
def create_demo_board():
    return [
        ["X", "O", "X"],
        ["", "X", "O"],
        ["O", "", ""]
    ]


# =========================
# COPY BOARD
# =========================
# Mục đích:
# - Mỗi bước trong UI cần lưu lại một trạng thái riêng.
# - Tránh việc bước sau làm thay đổi trạng thái đã ghi ở bước trước.
# =========================
def copy_board(board):
    copied = []

    for row in board:
        copied.append(row[:])

    return copied


# =========================
# CHUYỂN BOARD THÀNH KEY
# =========================
def board_key(board):
    return tuple(tuple(row) for row in board)


# =========================
# ĐẾM SỐ QUÂN CỜ
# =========================
def count_player(board, player):
    count = 0

    for row in board:
        for cell in row:
            if cell == player:
                count += 1

    return count


# =========================
# KIỂM TRA LƯỢT ĐI HỢP LỆ
# =========================
# Với caro 3x3:
# - X đi trước.
# - Số quân X bằng O hoặc hơn O đúng 1 quân là hợp lệ.
# =========================
def is_valid_turn_board(board):
    x_count = count_player(board, MAX_PLAYER)
    o_count = count_player(board, MIN_PLAYER)

    if o_count > x_count:
        return False

    if x_count - o_count > 1:
        return False

    return True


# =========================
# KIỂM TRA BÀN CỜ HỢP LỆ TỔNG QUÁT
# =========================
# Ngoài số lượt X/O, cần tránh các trạng thái tự tạo không thể xảy ra
# trong một ván cờ thật, ví dụ cả X và O cùng thắng.
# Hàm này dùng cho visualizer để báo lỗi sớm trước khi chạy thuật toán.
# =========================
def is_valid_game_board(board):
    if not is_valid_turn_board(board):
        return False

    x_count = count_player(board, MAX_PLAYER)
    o_count = count_player(board, MIN_PLAYER)

    x_win = False
    o_win = False

    for line in get_lines(board):
        if line.count(MAX_PLAYER) == WIN_LENGTH:
            x_win = True

        if line.count(MIN_PLAYER) == WIN_LENGTH:
            o_win = True

    # Một trạng thái hợp lệ không thể có cả hai bên cùng thắng.
    if x_win and o_win:
        return False

    # Nếu X thắng thì X phải vừa đi xong, nên X nhiều hơn O đúng 1 quân.
    if x_win and x_count != o_count + 1:
        return False

    # Nếu O thắng thì số quân X và O phải bằng nhau.
    if o_win and x_count != o_count:
        return False

    return True


# =========================
# XÁC ĐỊNH NGƯỜI ĐI TIẾP
# =========================
def get_current_player(board):
    x_count = count_player(board, MAX_PLAYER)
    o_count = count_player(board, MIN_PLAYER)

    if x_count <= o_count:
        return MAX_PLAYER

    return MIN_PLAYER


# =========================
# LẤY DANH SÁCH Ô TRỐNG
# =========================
def get_available_moves(board):
    moves = []

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                moves.append((i, j))

    return moves


# =========================
# SẮP XẾP NƯỚC ĐI
# =========================
# Đi giữa -> góc -> cạnh.
# Cách này giúp:
# - Minimax / Alpha-Beta dễ chọn nước đi đẹp hơn.
# - Alpha-Beta có nhiều cơ hội cắt tỉa hơn vì xét nhánh tốt trước.
# =========================
def move_priority(move):
    row, col = move
    center = BOARD_SIZE // 2

    if row == center and col == center:
        return 0

    if (row, col) in [(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]:
        return 1

    return 2


def order_moves(moves):
    return sorted(moves, key=move_priority)


# =========================
# ĐÁNH 1 NƯỚC ĐI
# =========================
def make_move(board, move, player):
    row, col = move
    new_board = copy_board(board)
    new_board[row][col] = player
    return new_board


# =========================
# ĐỔI LƯỢT
# =========================
def switch_player(player):
    if player == MAX_PLAYER:
        return MIN_PLAYER

    return MAX_PLAYER


# =========================
# LẤY CÁC DÒNG CÓ THỂ THẮNG
# =========================
# Với bàn 3x3 gồm:
# - 3 hàng
# - 3 cột
# - 2 đường chéo
# =========================
def get_lines(board):
    lines = []

    # Hàng ngang
    for i in range(BOARD_SIZE):
        line = []
        for j in range(BOARD_SIZE):
            line.append(board[i][j])
        lines.append(line)

    # Cột dọc
    for j in range(BOARD_SIZE):
        line = []
        for i in range(BOARD_SIZE):
            line.append(board[i][j])
        lines.append(line)

    # Chéo chính
    diagonal_1 = []
    for i in range(BOARD_SIZE):
        diagonal_1.append(board[i][i])
    lines.append(diagonal_1)

    # Chéo phụ
    diagonal_2 = []
    for i in range(BOARD_SIZE):
        diagonal_2.append(board[i][BOARD_SIZE - 1 - i])
    lines.append(diagonal_2)

    return lines


# =========================
# KIỂM TRA NGƯỜI THẮNG
# =========================
def get_winner(board):
    for line in get_lines(board):
        if line.count(MAX_PLAYER) == WIN_LENGTH:
            return MAX_PLAYER

        if line.count(MIN_PLAYER) == WIN_LENGTH:
            return MIN_PLAYER

    return None


# =========================
# KIỂM TRA BÀN CỜ ĐÃ ĐẦY CHƯA
# =========================
def is_board_full(board):
    return len(get_available_moves(board)) == 0


# =========================
# KIỂM TRA TRẠNG THÁI KẾT THÚC
# =========================
def is_terminal(board):
    if get_winner(board) is not None:
        return True

    if is_board_full(board):
        return True

    return False


# =========================
# ĐÁNH GIÁ TRẠNG THÁI KẾT THÚC
# =========================
# Điểm càng lớn càng có lợi cho X.
# Điểm càng nhỏ càng có lợi cho O.
# depth được dùng để ưu tiên thắng sớm và thua muộn.
# =========================
def terminal_score(board, depth):
    winner = get_winner(board)

    if winner == MAX_PLAYER:
        return 100 - depth

    if winner == MIN_PLAYER:
        return -100 + depth

    return 0


# =========================
# ĐIỂM HEURISTIC CHO TRẠNG THÁI CHƯA KẾT THÚC
# =========================
# Ý tưởng:
# - Một dòng chỉ có X và ô trống là cơ hội của MAX -> cộng điểm.
# - Một dòng chỉ có O và ô trống là nguy cơ từ MIN -> trừ điểm.
# - Dòng có 2 quân liên tiếp quan trọng hơn dòng có 1 quân.
# =========================
def heuristic_score(board):
    score = 0

    for line in get_lines(board):
        x_count = line.count(MAX_PLAYER)
        o_count = line.count(MIN_PLAYER)

        # Dòng đã bị chặn bởi cả X và O thì không còn nhiều giá trị.
        if x_count > 0 and o_count > 0:
            continue

        if x_count > 0 and o_count == 0:
            if x_count == 1:
                score += 3
            elif x_count == 2:
                score += 20

        if o_count > 0 and x_count == 0:
            if o_count == 1:
                score -= 3
            elif o_count == 2:
                score -= 20

    return score


# =========================
# HÀM ĐÁNH GIÁ CHUNG
# =========================
def evaluate_board(board, depth):
    if is_terminal(board):
        return terminal_score(board, depth)

    return heuristic_score(board)


# =========================
# FORMAT BOARD CHO LOG
# =========================
def format_cell(cell):
    if cell == EMPTY:
        return "."

    return cell


def format_board(board):
    lines = []

    for row in board:
        parts = []
        for cell in row:
            parts.append(format_cell(cell))
        lines.append(" ".join(parts))

    return "\n".join(lines)


# =========================
# FORMAT MOVE
# =========================
def format_move(move):
    if move is None:
        return "None"

    row, col = move
    return "(" + str(row + 1) + ", " + str(col + 1) + ")"


# =========================
# COPY DANH SÁCH ĐIỂM NƯỚC ĐI
# =========================
def copy_candidate_scores(candidate_scores):
    copied = []

    for item in candidate_scores:
        copied.append(item.copy())

    return copied
