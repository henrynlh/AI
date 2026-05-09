import random


def input_state():
    print("Nhập trạng thái 8-puzzle, mỗi dòng gồm 3 số, dùng số 0 làm ô trống.")
    print("Ví dụ:")
    print("1 2 3")
    print("4 0 6")
    print("7 5 8\n")

    state = []

    for i in range(3):
        while True:
            row_input = input(f"Nhập dòng {i + 1}: ")
            row = row_input.split()

            if len(row) != 3:
                print("Mỗi dòng phải có đúng 3 số. Nhập lại.")
                continue

            try:
                row = [int(x) for x in row]
            except ValueError:
                print("Chỉ được nhập số. Nhập lại.")
                continue

            state.append(row)
            break

    flat = [num for row in state for num in row]

    if sorted(flat) != list(range(9)):
        print("Trạng thái không hợp lệ. Phải có đủ các số từ 0 đến 8, không trùng.")
        return input_state()

    return state


def copy_state(state):
    return [row[:] for row in state]


def print_state(state):
    for row in state:
        print(row)


def state_key(state):
    return tuple(num for row in state for num in row)


def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None, None


def get_possible_moves(state):
    zero_x, zero_y = find_zero(state)

    possible_moves = []

    if zero_x > 0:
        possible_moves.append("up")

    if zero_x < 2:
        possible_moves.append("down")

    if zero_y > 0:
        possible_moves.append("left")

    if zero_y < 2:
        possible_moves.append("right")

    return possible_moves


def apply_move(state, move):
    new_state = copy_state(state)
    zero_x, zero_y = find_zero(new_state)

    new_x, new_y = zero_x, zero_y

    if move == "up":
        new_x = zero_x - 1
    elif move == "down":
        new_x = zero_x + 1
    elif move == "left":
        new_y = zero_y - 1
    elif move == "right":
        new_y = zero_y + 1

    new_state[zero_x][zero_y], new_state[new_x][new_y] = (
        new_state[new_x][new_y],
        new_state[zero_x][zero_y]
    )

    return new_state


def roll_one_move(state):
    possible_moves = get_possible_moves(state)

    print("Các bước có thể đi:", possible_moves)

    selected_move = random.choice(possible_moves)

    print("Roll chọn bước:", selected_move)

    new_state = apply_move(state, selected_move)

    return new_state, selected_move


if __name__ == "__main__":
    current_state = input_state()

    visited = {}
    visited[state_key(current_state)] = 0

    print("\nTrạng thái ban đầu:")
    print_state(current_state)

    step = 0

    while True:
        step += 1

        print(f"\n========== LẦN ROLL {step} ==========")

        current_state, selected_move = roll_one_move(current_state)

        print("Trạng thái sau khi đi:")
        print_state(current_state)

        key = state_key(current_state)

        if key in visited:
            duplicated_step = visited[key]

            print("\nDỪNG LẠI!")
            print("Lý do: Trạng thái này đã xuất hiện trước đó.")

            if duplicated_step == 0:
                print("Trạng thái hiện tại bị trùng với TRẠNG THÁI BAN ĐẦU.")
            else:
                print(f"Trạng thái hiện tại bị trùng với STEP {duplicated_step}.")

            print("Step hiện tại:", step)
            print("Step bị trùng:", duplicated_step)
            break

        visited[key] = step

    print("\nTổng số lần roll:", step)
