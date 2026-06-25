# =========================
# EXPECTIMAX - CỜ CA RÔ 3x3
# =========================
# Ý tưởng:
# - MAX là X: thuật toán chọn nước đi có kỳ vọng điểm lớn nhất.
# - Đối thủ O không bị xem là luôn tối ưu như Minimax.
# - Đối thủ O được mô hình hóa như CHANCE NODE: mỗi nước đi hợp lệ có cùng xác suất.
#
# Khi nào dùng Expectimax?
# - Khi đối thủ có yếu tố ngẫu nhiên.
# - Khi không muốn giả định đối thủ luôn chọn nước đi tối ưu nhất.
# =========================

from algorithms.caro_game import (
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


DEFAULT_RECORD_LIMIT = 700


# =========================
# THÊM STEP CHO UI
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
    candidate_scores=None,
    probability=None
):
    if len(steps) >= record_limit:
        return

    if manual_log is None:
        manual_log = []

    if candidate_scores is None:
        candidate_scores = []

    if player == MAX_PLAYER:
        node_type = "MAX"
    else:
        node_type = "CHANCE"

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
        "node_type": node_type,
        "probability": probability,
        "candidate_scores": copy_candidate_scores(candidate_scores),
        "manual_log": manual_log.copy(),
        "message": message
    })


# =========================
# EXPECTIMAX ĐỆ QUY
# =========================
# MAX node:
#   chọn max(expected_score)
# CHANCE node:
#   lấy trung bình điểm các nhánh con vì giả định đối thủ đi ngẫu nhiên đều.
# =========================
def expectimax_recursive(board, player, depth, max_depth, steps, stats, record_limit):
    stats["expanded_nodes"] += 1

    if player == MAX_PLAYER:
        node_name = "MAX node"
    else:
        node_name = "CHANCE node"

    add_step(
        steps,
        record_limit,
        "expand",
        board,
        player,
        depth,
        None,
        None,
        "Mở rộng " + node_name + " ở độ sâu " + str(depth) + ".",
        manual_log=[
            "Node hiện tại: " + node_name,
            "Người chơi hiện tại: " + player,
            "Board:\n" + format_board(board)
        ]
    )

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
            "Gặp node lá, trả điểm " + str(round(score, 3)) + ".",
            manual_log=[
                result_text,
                "score = " + str(round(score, 3))
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
            child_score, _ = expectimax_recursive(
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
                "score": round(child_score, 3),
                "note": "MAX chọn kỳ vọng lớn nhất"
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
            round(best_score, 3),
            "MAX chọn nước đi có expected score lớn nhất.",
            manual_log=[
                "MAX node: chọn max(expected_score).",
                "Best move = " + format_move(best_move),
                "Best expected score = " + str(round(best_score, 3))
            ],
            candidate_scores=candidate_scores
        )

        return best_score, best_move

    # =========================
    # CHANCE NODE
    # =========================
    # Mỗi nước đi của O có xác suất như nhau.
    # expected_score = trung bình cộng điểm các nhánh con.
    probability = 1 / len(moves)
    total_score = 0

    for move in moves:
        child_board = make_move(board, move, player)
        child_score, _ = expectimax_recursive(
            child_board,
            switch_player(player),
            depth + 1,
            max_depth,
            steps,
            stats,
            record_limit
        )

        total_score += probability * child_score

        candidate_scores.append({
            "move": move,
            "score": round(child_score, 3),
            "probability": round(probability, 3),
            "note": "p=" + str(round(probability, 3))
        })

        add_step(
            steps,
            record_limit,
            "chance",
            board,
            player,
            depth,
            move,
            round(total_score, 3),
            "CHANCE cộng điểm kỳ vọng từ một nhánh.",
            manual_log=[
                "Move ngẫu nhiên của O: " + format_move(move),
                "Xác suất p = " + str(round(probability, 3)),
                "Điểm nhánh = " + str(round(child_score, 3)),
                "Tổng kỳ vọng tạm thời = " + str(round(total_score, 3))
            ],
            candidate_scores=candidate_scores,
            probability=probability
        )

    expected_score = total_score

    add_step(
        steps,
        record_limit,
        "expectation",
        board,
        player,
        depth,
        None,
        round(expected_score, 3),
        "CHANCE node trả về điểm kỳ vọng.",
        manual_log=[
            "CHANCE node: expected_score = Σ p(move) * score(move).",
            "Số nước đi có thể: " + str(len(moves)),
            "Mỗi nước đi có xác suất: " + str(round(probability, 3)),
            "Expected score = " + str(round(expected_score, 3))
        ],
        candidate_scores=candidate_scores,
        probability=probability
    )

    return expected_score, None


# =========================
# HÀM CHÍNH GỌI EXPECTIMAX
# =========================
def expectimax_search(board=None, max_depth=5, record_limit=DEFAULT_RECORD_LIMIT):
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
        "Bắt đầu Expectimax.",
        manual_log=[
            "MAX = X.",
            "O được mô hình hóa là CHANCE node.",
            "Giả định các nước đi của O có xác suất bằng nhau.",
            "max_depth = " + str(max_depth),
            "Người đi tiếp: " + player,
            "Board ban đầu:\n" + format_board(board)
        ]
    )

    if is_terminal(board):
        score = evaluate_board(board, 0)
        best_move = None
    else:
        score, best_move = expectimax_recursive(
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
        round(score, 3),
        "Hoàn thành Expectimax.",
        manual_log=[
            "Best move = " + format_move(best_move),
            "Best expected score = " + str(round(score, 3)),
            "Expanded nodes = " + str(stats["expanded_nodes"])
        ]
    )

    return {
        "success": True,
        "algorithm": "Expectimax",
        "board": board,
        "final_board": final_board,
        "best_move": best_move,
        "best_score": round(score, 3),
        "current_player": player,
        "expanded_nodes": stats["expanded_nodes"],
        "steps": steps,
        "record_limit": record_limit,
        "max_depth": max_depth
    }


# Tên hàm ngắn để gọi tương tự các file thuật toán khác.
def expectimax(board=None, max_depth=5):
    return expectimax_search(board=board, max_depth=max_depth)
