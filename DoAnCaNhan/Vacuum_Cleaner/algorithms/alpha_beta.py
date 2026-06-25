# =========================
# ALPHA-BETA PRUNING - CỜ CA RÔ 3x3
# =========================
# Ý tưởng:
# - Vẫn dựa trên Minimax.
# - alpha: điểm tốt nhất hiện tại mà MAX chắc chắn đạt được.
# - beta: điểm tốt nhất hiện tại mà MIN có thể ép xuống.
# - Nếu alpha >= beta thì nhánh còn lại không thể ảnh hưởng đến quyết định cuối,
#   nên thuật toán cắt tỉa nhánh đó.
#
# So với Minimax:
# - Kết quả chọn nước đi giống Minimax nếu cùng hàm đánh giá và cùng độ sâu.
# - Số node mở rộng thường ít hơn nhờ cắt tỉa.
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
    alpha,
    beta,
    message,
    manual_log=None,
    candidate_scores=None,
    pruned=False
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
        "alpha": alpha,
        "beta": beta,
        "pruned": pruned,
        "node_type": "MAX" if player == MAX_PLAYER else "MIN",
        "candidate_scores": copy_candidate_scores(candidate_scores),
        "manual_log": manual_log.copy(),
        "message": message
    })


# =========================
# FORMAT ALPHA / BETA
# =========================
def format_bound(value):
    if value <= -10**8:
        return "-∞"

    if value >= 10**8:
        return "+∞"

    return str(value)


# =========================
# ALPHA-BETA ĐỆ QUY
# =========================
def alphabeta_recursive(board, player, depth, max_depth, alpha, beta, steps, stats, record_limit):
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
        alpha,
        beta,
        "Mở rộng node ở độ sâu " + str(depth) + ".",
        manual_log=[
            "Người chơi hiện tại: " + player,
            "alpha = " + format_bound(alpha) + ", beta = " + format_bound(beta),
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
            alpha,
            beta,
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
            child_score, _ = alphabeta_recursive(
                child_board,
                switch_player(player),
                depth + 1,
                max_depth,
                alpha,
                beta,
                steps,
                stats,
                record_limit
            )

            candidate_scores.append({
                "move": move,
                "score": child_score,
                "note": "Cập nhật alpha nếu tốt hơn"
            })

            if child_score > best_score:
                best_score = child_score
                best_move = move

            if best_score > alpha:
                alpha = best_score

            add_step(
                steps,
                record_limit,
                "update",
                board,
                player,
                depth,
                move,
                best_score,
                alpha,
                beta,
                "MAX cập nhật alpha.",
                manual_log=[
                    "Vừa xét move " + format_move(move) + " có score = " + str(child_score),
                    "best_score = " + str(best_score),
                    "alpha = max(alpha, best_score) = " + format_bound(alpha),
                    "beta = " + format_bound(beta)
                ],
                candidate_scores=candidate_scores
            )

            # Điều kiện cắt tỉa
            if alpha >= beta:
                remaining_moves = []
                for later_move in moves:
                    if later_move not in [item["move"] for item in candidate_scores]:
                        remaining_moves.append(later_move)

                add_step(
                    steps,
                    record_limit,
                    "prune",
                    board,
                    player,
                    depth,
                    move,
                    best_score,
                    alpha,
                    beta,
                    "Cắt tỉa nhánh vì alpha >= beta.",
                    manual_log=[
                        "Điều kiện cắt tỉa: alpha >= beta.",
                        "alpha = " + format_bound(alpha) + ", beta = " + format_bound(beta),
                        "Các nhánh còn lại không cần xét vì MIN sẽ không cho đi vào nhánh này."
                    ],
                    candidate_scores=candidate_scores,
                    pruned=True
                )
                break

        add_step(
            steps,
            record_limit,
            "choose",
            board,
            player,
            depth,
            best_move,
            best_score,
            alpha,
            beta,
            "MAX chọn nước đi tốt nhất sau khi xét/cắt tỉa.",
            manual_log=[
                "Best move = " + format_move(best_move),
                "Best score = " + str(best_score),
                "alpha cuối = " + format_bound(alpha),
                "beta cuối = " + format_bound(beta)
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
        child_score, _ = alphabeta_recursive(
            child_board,
            switch_player(player),
            depth + 1,
            max_depth,
            alpha,
            beta,
            steps,
            stats,
            record_limit
        )

        candidate_scores.append({
            "move": move,
            "score": child_score,
            "note": "Cập nhật beta nếu nhỏ hơn"
        })

        if child_score < best_score:
            best_score = child_score
            best_move = move

        if best_score < beta:
            beta = best_score

        add_step(
            steps,
            record_limit,
            "update",
            board,
            player,
            depth,
            move,
            best_score,
            alpha,
            beta,
            "MIN cập nhật beta.",
            manual_log=[
                "Vừa xét move " + format_move(move) + " có score = " + str(child_score),
                "best_score = " + str(best_score),
                "alpha = " + format_bound(alpha),
                "beta = min(beta, best_score) = " + format_bound(beta)
            ],
            candidate_scores=candidate_scores
        )

        if alpha >= beta:
            add_step(
                steps,
                record_limit,
                "prune",
                board,
                player,
                depth,
                move,
                best_score,
                alpha,
                beta,
                "Cắt tỉa nhánh vì alpha >= beta.",
                manual_log=[
                    "Điều kiện cắt tỉa: alpha >= beta.",
                    "alpha = " + format_bound(alpha) + ", beta = " + format_bound(beta),
                    "Các nhánh còn lại không cần xét vì MAX đã có lựa chọn tốt hơn ở nơi khác."
                ],
                candidate_scores=candidate_scores,
                pruned=True
            )
            break

    add_step(
        steps,
        record_limit,
        "choose",
        board,
        player,
        depth,
        best_move,
        best_score,
        alpha,
        beta,
        "MIN chọn nước đi tốt nhất sau khi xét/cắt tỉa.",
        manual_log=[
            "Best move = " + format_move(best_move),
            "Best score = " + str(best_score),
            "alpha cuối = " + format_bound(alpha),
            "beta cuối = " + format_bound(beta)
        ],
        candidate_scores=candidate_scores
    )

    return best_score, best_move


# =========================
# HÀM CHÍNH GỌI ALPHA-BETA
# =========================
def alphabeta_search(board=None, max_depth=5, record_limit=DEFAULT_RECORD_LIMIT):
    if board is None:
        board = create_demo_board()

    board = copy_board(board)
    player = get_current_player(board)
    steps = []
    stats = {
        "expanded_nodes": 0
    }

    alpha = -10**9
    beta = 10**9

    add_step(
        steps,
        record_limit,
        "start",
        board,
        player,
        0,
        None,
        None,
        alpha,
        beta,
        "Bắt đầu Alpha-Beta Pruning.",
        manual_log=[
            "MAX = X, MIN = O.",
            "Alpha-Beta là Minimax có cắt tỉa.",
            "alpha ban đầu = -∞, beta ban đầu = +∞.",
            "max_depth = " + str(max_depth),
            "Người đi tiếp: " + player,
            "Board ban đầu:\n" + format_board(board)
        ]
    )

    if is_terminal(board):
        score = evaluate_board(board, 0)
        best_move = None
    else:
        score, best_move = alphabeta_recursive(
            board,
            player,
            0,
            max_depth,
            alpha,
            beta,
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
        alpha,
        beta,
        "Hoàn thành Alpha-Beta Pruning.",
        manual_log=[
            "Best move = " + format_move(best_move),
            "Best score = " + str(score),
            "Expanded nodes = " + str(stats["expanded_nodes"])
        ]
    )

    return {
        "success": True,
        "algorithm": "Alpha-Beta Pruning",
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
def alphabeta(board=None, max_depth=5):
    return alphabeta_search(board=board, max_depth=max_depth)
