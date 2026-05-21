import random


# =========================
# RANDOM TRẠNG THÁI BAN ĐẦU
# =========================
def random_floor(m, n):
    floor = []

    for i in range(m):
        row = []
        for j in range(n):
            row.append(random.choice([0, 1]))  # 0 = sạch, 1 = bẩn
        floor.append(row)

    # Random vị trí ban đầu của máy hút bụi
    vx = random.randint(0, m - 1)
    vy = random.randint(0, n - 1)

    # Gán V vào ma trận
    floor[vx][vy] = "V"

    return floor


# =========================
# OUTPUT / FORMAT
# =========================
def output_floor(floor):
    for row in floor:
        print(row)


def format_floor(floor):
    return "\n".join([" ".join(map(str, row)) for row in floor])


# =========================
# CÁC HÀM XỬ LÝ MA TRẬN
# =========================
def copy_floor(floor):
    return [row[:] for row in floor]


def goal(floor):
    # Trạng thái đích: không còn ô bẩn 1
    for row in floor:
        for cell in row:
            if cell == 1:
                return False
    return True


def find_vacuum(floor):
    for i in range(len(floor)):
        for j in range(len(floor[0])):
            if floor[i][j] == "V":
                return i, j
    return None


def get_possible_moves(floor):
    vx, vy = find_vacuum(floor)

    m = len(floor)
    n = len(floor[0])

    moves = []

    # Không có vật cản, chỉ kiểm tra biên
    if vx > 0:
        moves.append("UP")

    if vx < m - 1:
        moves.append("DOWN")

    if vy > 0:
        moves.append("LEFT")

    if vy < n - 1:
        moves.append("RIGHT")

    return moves


def apply_move(pos, action):
    vx, vy = pos

    if action == "UP":
        vx -= 1

    if action == "DOWN":
        vx += 1

    if action == "LEFT":
        vy -= 1

    if action == "RIGHT":
        vy += 1

    return vx, vy


def move_vacuum(floor, action):
    new_floor = copy_floor(floor)

    old_vx, old_vy = find_vacuum(new_floor)
    new_vx, new_vy = apply_move((old_vx, old_vy), action)

    # Ô cũ sau khi máy rời đi thì thành sạch
    new_floor[old_vx][old_vy] = 0

    # Ô mới dù là 0 hay 1 thì máy tới đó sẽ hút sạch và hiển thị V
    new_floor[new_vx][new_vy] = "V"

    return new_floor


def state_key(floor):
    # Chuyển ma trận list thành tuple để lưu vào set reached
    return tuple(tuple(row) for row in floor)
