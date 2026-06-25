# =========================
# MINIMAX - CỜ CA RÔ 3x3
# =========================
# Ý tưởng:
# - MAX là X: cố gắng chọn nước đi làm điểm lớn nhất.
# - MIN là O: cố gắng chọn nước đi làm điểm nhỏ nhất.
# - Thuật toán giả định hai bên đều chơi tối ưu.
#
# Dùng cho visualizer:
# - Lưu lại từng bước mở rộng node.
# - Lưu điểm của từng nước đi ứng viên.
# - Trả về best_move để UI tô nổi bật nước đi thuật toán chọn.
# =========================

from algorithms.caro_game import (
    EMPTY,
    MAX_PLAYER,
    MIN_PLAYER,
    copy_board,
    copy_candidate_scores,
    create_demo_board,
    evaluate_board,
    format_board,
    format_move,
    get_available_moves,
    get_current_player,
    get_winner,
    is_terminal,
    make_move,
    order_moves,
    switch_player
)


# =========================
# GIỚI HẠN SỐ STEP GHI VÀO UI
# =========================
# Cây trò chơi có thể rất lớn, nên thuật toán vẫn đếm expanded_nodes đầy đủ,
# nhưng chỉ ghi một phần step đầu tiên để UI không bị quá tải.
# =========================
DEFAULT_RECORD_LIMIT = 700


# =========================
# COPY STEP BOARD
# =========================
def add_step(
    steps,
    record_limit,
    step_type,
    board,
    player,
    depth,
    move,
    score,
    message,
    manual_log=None,
    candidate_scores=None
):
    if len(steps) >= record_limit:
        return

    if manual_log is None:
        manual_log = []

    if candidate_scores is None:
        candidate_scores = []

    steps.append({
        "type": step_type,
        "board": copy_board(board),
        "player": player,
        "depth": depth,
        "move": move,
        "score": score,
        "alpha": None,
        "beta": None,
        "pruned": False,
        "node_type": "MAX" if player == MAX_PLAYER else "MIN",
        "candidate_scores": copy_candidate_scores(candidate_scores),
        "manual_log": manual_log.copy(),
        "message": message
    })


# =========================
# MINIMAX ĐỆ QUY
# =========================
# Tham số:
# - board: trạng thái bàn cờ hiện tại
# - player: người chơi sắp đi ở node hiện tại
# - depth: độ sâu hiện tại trong cây tìm kiếm
# - max_depth: giới hạn độ sâu
#
# Trả về:
# - score: điểm tốt nhất tại node
# - best_move: nước đi tốt nhất tại node đó
# =========================
def minimax_recursive(board, player, depth, max_depth, steps, stats, record_limit):
    stats["expanded_nodes"] += 1

    add_step(
        steps,
        record_limit,
        "expand",
        board,
        player,
        depth,
        None,
        None,
        "Mở rộng node ở độ sâu " + str(depth) + ".",
        manual_log=[
            "Người chơi hiện tại: " + player,
            "Board:\n" + format_board(board)
        ]
    )

    # Điều kiện dừng: thắng / thua / hòa / đạt giới hạn độ sâu.
    if is_terminal(board) or depth == max_depth:
        score = evaluate_board(board, depth)
        winner = get_winner(board)

        if winner is None:
            result_text = "Chưa có người thắng hoặc hòa. Dùng heuristic để đánh giá."
        else:
            result_text = "Người thắng: " + winner

        add_step(
            steps,
            record_limit,
            "leaf",
            board,
            player,
            depth,
            None,
            score,
            "Gặp node lá, trả điểm " + str(score) + ".",
            manual_log=[
                result_text,
                "score = " + str(score)
            ]
        )

        return score, None

    moves = order_moves(get_available_moves(board))
    candidate_scores = []

    # =========================
    # MAX NODE
    # =========================
    if player == MAX_PLAYER:
        best_score = -10**9
        best_move = None

        for move in moves:
            child_board = make_move(board, move, player)
            child_score, _ = minimax_recursive(
                child_board,
                switch_player(player),
                depth + 1,
                max_depth,
                steps,
                stats,
                record_limit
            )

            candidate_scores.append({
                "move": move,
                "score": child_score,
                "note": "MAX chọn điểm lớn nhất"
            })

            if child_score > best_score:
                best_score = child_score
                best_move = move

        add_step(
            steps,
            record_limit,
            "choose",
            board,
            player,
            depth,
            best_move,
            best_score,
            "MAX chọn nước đi có điểm lớn nhất.",
            manual_log=[
                "MAX node: chọn max(score).",
                "Best move = " + format_move(best_move),
                "Best score = " + str(best_score)
            ],
            candidate_scores=candidate_scores
        )

        return best_score, best_move

    # =========================
    # MIN NODE
    # =========================
    best_score = 10**9
    best_move = None

    for move in moves:
        child_board = make_move(board, move, player)
        child_score, _ = minimax_recursive(
            child_board,
            switch_player(player),
            depth + 1,
            max_depth,
            steps,
            stats,
            record_limit
        )

        candidate_scores.append({
            "move": move,
            "score": child_score,
            "note": "MIN chọn điểm nhỏ nhất"
        })

        if child_score < best_score:
            best_score = child_score
            best_move = move

    add_step(
        steps,
        record_limit,
        "choose",
        board,
        player,
        depth,
        best_move,
        best_score,
        "MIN chọn nước đi có điểm nhỏ nhất.",
        manual_log=[
            "MIN node: chọn min(score).",
            "Best move = " + format_move(best_move),
            "Best score = " + str(best_score)
        ],
        candidate_scores=candidate_scores
    )

    return best_score, best_move


# =========================
# HÀM CHÍNH GỌI MINIMAX
# =========================
def minimax_search(board=None, max_depth=5, record_limit=DEFAULT_RECORD_LIMIT):
    if board is None:
        board = create_demo_board()

    board = copy_board(board)
    player = get_current_player(board)
    steps = []
    stats = {
        "expanded_nodes": 0
    }

    add_step(
        steps,
        record_limit,
        "start",
        board,
        player,
        0,
        None,
        None,
        "Bắt đầu Minimax.",
        manual_log=[
            "MAX = X, MIN = O.",
            "Giả định hai bên đều đi tối ưu.",
            "max_depth = " + str(max_depth),
            "Người đi tiếp: " + player,
            "Board ban đầu:\n" + format_board(board)
        ]
    )

    if is_terminal(board):
        score = evaluate_board(board, 0)
        best_move = None
    else:
        score, best_move = minimax_recursive(
            board,
            player,
            0,
            max_depth,
            steps,
            stats,
            record_limit
        )

    if best_move is None:
        final_board = copy_board(board)
    else:
        final_board = make_move(board, best_move, player)

    add_step(
        steps,
        record_limit,
        "done",
        final_board,
        player,
        0,
        best_move,
        score,
        "Hoàn thành Minimax.",
        manual_log=[
            "Best move = " + format_move(best_move),
            "Best score = " + str(score),
            "Expanded nodes = " + str(stats["expanded_nodes"])
        ]
    )

    return {
        "success": True,
        "algorithm": "Minimax",
        "board": board,
        "final_board": final_board,
        "best_move": best_move,
        "best_score": score,
        "current_player": player,
        "expanded_nodes": stats["expanded_nodes"],
        "steps": steps,
        "record_limit": record_limit,
        "max_depth": max_depth
    }


# Tên hàm ngắn để gọi tương tự các file thuật toán khác.
def minimax(board=None, max_depth=5):
    return minimax_search(board=board, max_depth=max_depth)
