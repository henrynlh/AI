# 🤖 Đồ án cá nhân: Vacuum Cleaner Search

## 1. Giới thiệu

Đây là đồ án cá nhân môn **Trí Tuệ Nhân Tạo**, xây dựng chương trình mô phỏng bài toán **Vacuum Cleaner Problem** bằng ngôn ngữ **Python**.  
Chương trình cho phép tạo ngẫu nhiên một môi trường dạng ma trận, trong đó máy hút bụi di chuyển qua các ô để làm sạch toàn bộ các ô bẩn.

Ở giai đoạn hiện tại, đồ án tập trung vào nhóm thuật toán **tìm kiếm không có thông tin**, cụ thể là:

- **BFS** - Breadth-First Search
- **DFS** - Depth-First Search

Mỗi thuật toán được cài đặt theo 2 dạng xử lý khác nhau:

- **Dạng 1**: Lấy node ra khỏi frontier rồi mới kiểm tra goal.
- **Dạng 2**: Vừa sinh trạng thái con thì kiểm tra goal ngay.

---

## 2. Mục tiêu đồ án

Mục tiêu của đồ án là xây dựng một chương trình mô phỏng quá trình giải bài toán máy hút bụi tự động bằng các thuật toán tìm kiếm cơ bản trong AI.

Thông qua đồ án, sinh viên có thể:

- Hiểu cách mô hình hóa một bài toán AI dưới dạng bài toán tìm kiếm.
- Biết cách biểu diễn trạng thái, hành động, trạng thái đích và lời giải.
- Cài đặt và so sánh cách hoạt động của BFS và DFS.
- Phân biệt hai cách kiểm tra goal trong quá trình tìm kiếm.
- Xây dựng giao diện trực quan bằng Tkinter để quan sát quá trình thuật toán hoạt động.

---

## 3. Mô tả bài toán

Bài toán mô phỏng một máy hút bụi di chuyển trong một ma trận kích thước `m x n`.

Mỗi ô trong ma trận có thể thuộc một trong các trạng thái sau:

| Ký hiệu | Ý nghĩa |
|--------|---------|
| `0` | Ô sạch |
| `1` | Ô bẩn |
| `V` | Vị trí hiện tại của máy hút bụi |

Máy hút bụi có thể di chuyển theo 4 hướng:

- Lên
- Xuống
- Trái
- Phải

Khi máy hút bụi đi đến một ô, ô đó được xem như đã được làm sạch.

---

## 4. Thành phần của bài toán tìm kiếm

### 4.1. Không gian trạng thái

Không gian trạng thái là tập hợp tất cả các cấu hình có thể có của ma trận, bao gồm:

- Vị trí hiện tại của máy hút bụi.
- Trạng thái sạch hoặc bẩn của từng ô.

Mỗi trạng thái được biểu diễn bằng một ma trận hai chiều trong Python.

Ví dụ:

```python
[
    [0, 1, 0],
    [1, "V", 1],
    [0, 0, 1]
]
```

### 4.2. Trạng thái ban đầu

Trạng thái ban đầu được tạo ngẫu nhiên bằng hàm `random_floor(m, n)`.

Trong đó:

- `m` là số dòng.
- `n` là số cột.
- Các ô được random giá trị `0` hoặc `1`.
- Một vị trí ngẫu nhiên được chọn làm vị trí ban đầu của máy hút bụi `V`.

### 4.3. Trạng thái đích

Trạng thái đích là trạng thái mà trong ma trận không còn ô bẩn nào.

Nói cách khác, trạng thái được xem là goal khi không còn giá trị `1` trong ma trận.

```python
def goal(floor):
    for row in floor:
        for cell in row:
            if cell == 1:
                return False
    return True
```

### 4.4. Hành động

Tại mỗi trạng thái, máy hút bụi có thể thực hiện các hành động hợp lệ:

- `UP`
- `DOWN`
- `LEFT`
- `RIGHT`

Một hành động chỉ hợp lệ nếu không làm máy hút bụi đi ra ngoài biên của ma trận.

### 4.5. Chi phí

Ở giai đoạn hiện tại, mỗi bước di chuyển được xem là có chi phí bằng nhau.  
Do đó, BFS có thể tìm lời giải theo số bước ngắn nhất trong trường hợp không gian trạng thái được duyệt đầy đủ.

### 4.6. Lời giải

Lời giải là một chuỗi các trạng thái từ trạng thái ban đầu đến trạng thái đích.

Trong chương trình, lời giải được lưu trong thuộc tính:

```python
"path": [initial_floor, state_1, state_2, ..., goal_state]
```

---

## 5. Các thuật toán đã cài đặt

## 5.1. Breadth-First Search - BFS

BFS là thuật toán tìm kiếm theo chiều rộng. Thuật toán mở rộng các trạng thái theo từng mức, ưu tiên các trạng thái được sinh ra trước.

Trong đồ án, BFS được cài đặt bằng hàng đợi `deque`.

### BFS Dạng 1

Ở dạng này, thuật toán lấy node ra khỏi frontier trước, sau đó mới kiểm tra node đó có phải goal hay không.

Quy trình chính:

1. Đưa trạng thái ban đầu vào frontier.
2. Lấy node đầu tiên ra khỏi queue.
3. Kiểm tra goal.
4. Nếu chưa đạt goal, sinh các trạng thái con.
5. Đưa các trạng thái con chưa xét vào frontier.
6. Lặp lại cho đến khi tìm được lời giải hoặc frontier rỗng.

### BFS Dạng 2

Ở dạng này, thuật toán kiểm tra goal ngay khi sinh ra trạng thái con.

Quy trình chính:

1. Kiểm tra riêng trạng thái ban đầu.
2. Đưa trạng thái ban đầu vào frontier.
3. Lấy node ra khỏi queue.
4. Sinh các trạng thái con.
5. Nếu trạng thái con là goal, trả về lời giải ngay.
6. Nếu chưa đạt goal, thêm trạng thái con vào frontier.

### Nhận xét BFS

- BFS phù hợp khi cần tìm lời giải có số bước ngắn.
- BFS dễ hiểu và phù hợp để minh họa khái niệm frontier, reached và path.
- Nhược điểm là có thể tốn bộ nhớ khi kích thước ma trận tăng.

---

## 5.2. Depth-First Search - DFS

DFS là thuật toán tìm kiếm theo chiều sâu. Thuật toán ưu tiên mở rộng một nhánh sâu nhất có thể trước khi quay lui.

Trong đồ án, DFS được cài đặt bằng danh sách Python đóng vai trò như stack.

### DFS Dạng 1

Ở dạng này, thuật toán lấy node ra khỏi frontier trước, sau đó mới kiểm tra goal.

Quy trình chính:

1. Đưa trạng thái ban đầu vào stack.
2. Lấy node cuối cùng ra khỏi stack.
3. Kiểm tra goal.
4. Nếu chưa đạt goal, sinh các trạng thái con.
5. Thêm trạng thái con chưa xét vào stack.
6. Lặp lại cho đến khi tìm được lời giải hoặc frontier rỗng.

### DFS Dạng 2

Ở dạng này, thuật toán kiểm tra goal ngay khi sinh trạng thái con.

Quy trình chính:

1. Kiểm tra riêng trạng thái ban đầu.
2. Đưa trạng thái ban đầu vào stack.
3. Lấy node ra khỏi stack.
4. Sinh các trạng thái con.
5. Nếu trạng thái con là goal, trả về lời giải ngay.
6. Nếu chưa đạt goal, thêm trạng thái con vào stack.

### Nhận xét DFS

- DFS có cách cài đặt đơn giản.
- DFS thường sử dụng ít bộ nhớ hơn BFS trong nhiều trường hợp.
- DFS không đảm bảo tìm được lời giải ngắn nhất.
- Thứ tự sinh hành động ảnh hưởng lớn đến đường đi tìm được.

---

## 6. So sánh Dạng 1 và Dạng 2

| Tiêu chí | Dạng 1 | Dạng 2 |
|---------|--------|--------|
| Thời điểm kiểm tra goal | Khi node được lấy ra khỏi frontier | Ngay khi sinh trạng thái con |
| Trạng thái ban đầu | Được kiểm tra trong vòng lặp | Được kiểm tra riêng trước vòng lặp |
| Khả năng dừng sớm | Có thể chậm hơn một chút | Có thể dừng sớm hơn khi child là goal |
| Ý nghĩa học thuật | Bám sát mô hình graph search truyền thống | Minh họa cách tối ưu thời điểm kiểm tra goal |

---

## 7. Cấu trúc thư mục hiện tại

```text
project/
│
├── main.py
│
├── core/
│   └── vacuum_problem.py
│
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   └── algorithm_manager.py
│
└── ui/
    └── vacuum_ui.py
```

### Vai trò từng file

| File | Chức năng |
|------|-----------|
| `main.py` | Điểm bắt đầu chương trình, khởi tạo Tkinter và giao diện chính |
| `core/vacuum_problem.py` | Chứa các hàm xử lý bài toán như random ma trận, kiểm tra goal, di chuyển máy hút bụi |
| `algorithms/bfs.py` | Cài đặt BFS Dạng 1 và BFS Dạng 2 |
| `algorithms/dfs.py` | Cài đặt DFS Dạng 1 và DFS Dạng 2 |
| `algorithms/algorithm_manager.py` | Quản lý danh sách thuật toán và điều phối hàm solve |
| `ui/vacuum_ui.py` | Xây dựng giao diện người dùng bằng Tkinter |

---

## 8. Giao diện chương trình

Giao diện được xây dựng bằng thư viện **Tkinter**.

Các chức năng hiện có:

- Nhập số dòng và số cột của ma trận.
- Tạo trạng thái ban đầu ngẫu nhiên.
- Chọn thuật toán BFS hoặc DFS.
- Chọn dạng giải: Dạng 1 hoặc Dạng 2.
- Điều chỉnh tốc độ chạy.
- Hiển thị từng bước di chuyển của máy hút bụi.
- Hiển thị trạng thái kết quả.
- Hiển thị process log trong quá trình giải.
- Dừng hoặc reset chương trình.

---

## 9. Hướng dẫn chạy chương trình

### 9.1. Yêu cầu môi trường

- Python 3.x
- Tkinter

Tkinter thường được cài sẵn cùng Python. Nếu chưa có, cần cài thêm theo hệ điều hành đang sử dụng.

### 9.2. Cách chạy

Mở terminal tại thư mục project và chạy:

```bash
python main.py
```

Sau khi chương trình mở lên:

1. Nhập số dòng và số cột.
2. Bấm **Random State** để tạo môi trường.
3. Chọn thuật toán.
4. Chọn dạng giải.
5. Bấm **Solve** để bắt đầu tìm lời giải.
6. Quan sát quá trình chạy trong phần hiển thị ma trận và process log.

---

## 10. Kết quả hiện tại

Ở tiến độ hiện tại, đồ án đã hoàn thành các nội dung sau:

- Xây dựng được mô hình bài toán Vacuum Cleaner dưới dạng bài toán tìm kiếm.
- Cài đặt trạng thái ban đầu ngẫu nhiên theo ma trận `m x n`.
- Cài đặt điều kiện goal: không còn ô bẩn.
- Cài đặt hành động di chuyển máy hút bụi theo 4 hướng.
- Cài đặt BFS Dạng 1 và BFS Dạng 2.
- Cài đặt DFS Dạng 1 và DFS Dạng 2.
- Xây dựng giao diện Tkinter để trực quan hóa quá trình giải.
- Hiển thị số bước, thời gian thực thi và log quá trình tìm kiếm.

---

## 11. Hạn chế hiện tại

Do đồ án đang trong quá trình phát triển, chương trình hiện còn một số hạn chế:

- Mới cài đặt BFS và DFS, chưa mở rộng sang các thuật toán khác.
- Chưa có biểu đồ so sánh hiệu suất giữa các thuật toán.
- Chưa lưu kết quả chạy ra file.
- Với ma trận lớn, BFS hoặc DFS có thể mất nhiều thời gian do không gian trạng thái tăng nhanh.
- Nút Stop hiện chủ yếu dừng quá trình hiển thị, chưa can thiệp sâu vào thuật toán nếu thuật toán đang chạy lâu.

---

## 12. Hướng phát triển

Trong các giai đoạn tiếp theo, đồ án có thể mở rộng theo các hướng:

- Bổ sung các thuật toán tìm kiếm khác như UCS, Greedy Search, A*.
- Thêm heuristic để hỗ trợ nhóm tìm kiếm có thông tin.
- Bổ sung thống kê số trạng thái đã duyệt.
- Vẽ biểu đồ so sánh thời gian chạy, số bước và bộ nhớ.
- Cải thiện giao diện để chạy mượt hơn với ma trận lớn.
- Cho phép người dùng tự thiết lập trạng thái ban đầu thay vì chỉ random.
- Lưu log hoặc kết quả thực nghiệm ra file.

---

## 13. Kết luận

Đồ án hiện đã hoàn thành phần nền tảng của một bài toán tìm kiếm trong Trí tuệ nhân tạo.  
Thông qua bài toán Vacuum Cleaner, chương trình đã thể hiện được cách xây dựng không gian trạng thái, trạng thái ban đầu, trạng thái đích, hành động và lời giải.

Ở giai đoạn hiện tại, BFS và DFS là hai thuật toán chính được sử dụng để minh họa sự khác nhau giữa tìm kiếm theo chiều rộng và tìm kiếm theo chiều sâu. Việc bổ sung hai dạng kiểm tra goal giúp làm rõ hơn ảnh hưởng của thời điểm kiểm tra mục tiêu trong quá trình tìm kiếm.

---

## 14. Tài liệu tham khảo

1. Russell, S., & Norvig, P. (2016). *Artificial Intelligence: A Modern Approach* (3rd ed.). Pearson.
2. GeeksforGeeks. (n.d.). Breadth First Search or BFS for a Graph.
3. GeeksforGeeks. (n.d.). Depth First Search or DFS for a Graph.
4. Python Software Foundation. (n.d.). Tkinter — Python interface to Tcl/Tk.

---

## 👨‍💻 Tác giả

**Họ và tên:** Nguyễn Lê Huy  
**MSSV:** 24110221  
**Môn học:** Trí Tuệ Nhân Tạo  
**Giảng viên hướng dẫn:** Phan Thị Huyền Trang