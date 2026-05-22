# 🤖 Đồ án cá nhân: Vacuum Cleaner Search

## 1. Giới thiệu

Đây là đồ án cá nhân môn **Trí Tuệ Nhân Tạo**, xây dựng chương trình mô phỏng bài toán **Vacuum Cleaner Problem** bằng ngôn ngữ **Python**.  
Chương trình cho phép tạo ngẫu nhiên một môi trường dạng ma trận, trong đó máy hút bụi di chuyển qua các ô để làm sạch toàn bộ các ô bẩn.

Ở giai đoạn hiện tại, đồ án tập trung vào nhóm thuật toán **tìm kiếm không có thông tin** (*Uninformed Search*), còn gọi là **tìm kiếm mù**. Đây là nhóm thuật toán không sử dụng tri thức bổ sung hay hàm heuristic để định hướng quá trình tìm kiếm, mà chỉ dựa trên mô hình bài toán gồm trạng thái ban đầu, hành động, chi phí và trạng thái đích.

Các thuật toán đã được cài đặt gồm:

- **BFS** - Breadth-First Search
- **DFS** - Depth-First Search
- **UCS** - Uniform Cost Search
- **IDS** - Iterative Deepening Search

Mỗi thuật toán được cài đặt theo 2 dạng xử lý khác nhau:

- **Dạng 1**: Lấy node ra khỏi frontier rồi mới kiểm tra goal.
- **Dạng 2**: Vừa sinh trạng thái con thì kiểm tra goal ngay. (trừ UCS)

Việc triển khai hai dạng kiểm tra goal giúp quan sát rõ hơn sự khác nhau về thời điểm phát hiện trạng thái đích, đồng thời hỗ trợ so sánh cách hoạt động của các thuật toán tìm kiếm cơ bản trong cùng một môi trường bài toán.

---

## 2. Mục tiêu đồ án

Mục tiêu của đồ án là xây dựng một chương trình mô phỏng quá trình giải bài toán máy hút bụi tự động bằng các thuật toán tìm kiếm cơ bản trong AI.

Thông qua đồ án, ta có thể:

- Hiểu cách mô hình hóa một bài toán AI dưới dạng bài toán tìm kiếm.
- Biết cách biểu diễn trạng thái, hành động, trạng thái đích, chi phí và lời giải.
- Cài đặt và so sánh cách hoạt động của BFS, DFS, UCS và IDS.
- Phân biệt nhóm thuật toán tìm kiếm không có thông tin với nhóm tìm kiếm có thông tin.
- Phân biệt hai cách kiểm tra goal trong quá trình tìm kiếm.
- Quan sát ảnh hưởng của cấu trúc frontier đến thứ tự mở rộng trạng thái.
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

Đối với các thuật toán BFS, DFS và IDS, mỗi hành động di chuyển có thể được xem là một bước trong quá trình tìm kiếm.

Riêng với **UCS**, chi phí được xác định dựa trên **số ô bẩn còn lại trong trạng thái**. Trạng thái có số ô bẩn ít hơn sẽ có chi phí thấp hơn và được ưu tiên mở rộng trước.

Cách mô hình hóa này giúp UCS ưu tiên các trạng thái tiến gần hơn đến mục tiêu làm sạch toàn bộ ma trận, nhưng vẫn thuộc nhóm **tìm kiếm không có thông tin** vì thuật toán không sử dụng heuristic ước lượng khoảng cách đến goal, mà chỉ dựa trên chi phí được định nghĩa trực tiếp từ trạng thái hiện tại.

### 4.6. Lời giải

Lời giải là một chuỗi các trạng thái từ trạng thái ban đầu đến trạng thái đích.

Trong chương trình, lời giải được lưu trong thuộc tính:

```python
"path": [initial_floor, state_1, state_2, ..., goal_state]
```

---

## 5. Nhóm thuật toán tìm kiếm không có thông tin

Các thuật toán trong đồ án hiện thuộc nhóm **tìm kiếm không có thông tin** (*Uninformed Search*).

Nhóm thuật toán này có đặc điểm:

- Không sử dụng heuristic để ước lượng trạng thái nào gần goal hơn.
- Chỉ dựa vào trạng thái ban đầu, tập hành động, kiểm tra goal và chi phí nếu có.
- Có thể áp dụng cho nhiều bài toán tìm kiếm tổng quát.
- Dễ cài đặt và phù hợp để minh họa nền tảng của AI search.

Bốn thuật toán được sử dụng trong đồ án gồm:

| Thuật toán | Tên đầy đủ | Cấu trúc frontier | Đặc điểm chính |
|-----------|------------|-------------------|----------------|
| BFS | Breadth-First Search | Queue | Mở rộng theo từng mức, thường tìm lời giải ít bước nhất nếu chi phí các bước bằng nhau |
| DFS | Depth-First Search | Stack | Đi sâu theo một nhánh trước, tiết kiệm bộ nhớ hơn BFS nhưng không đảm bảo tối ưu |
| UCS | Uniform Cost Search | Priority Queue | Luôn mở rộng node có chi phí thấp nhất |
| IDS | Iterative Deepening Search | Depth-Limited DFS lặp lại | Kết hợp ưu điểm bộ nhớ của DFS và tính đầy đủ theo mức của BFS |

---

## 6. Các thuật toán đã cài đặt

## 6.1. Breadth-First Search - BFS

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
- BFS đầy đủ nếu không gian trạng thái hữu hạn và có cơ chế tránh lặp.
- BFS có thể tìm lời giải tối ưu theo số bước khi mọi hành động có chi phí bằng nhau.
- Nhược điểm chính là có thể tốn nhiều bộ nhớ khi kích thước ma trận tăng.

---

## 6.2. Depth-First Search - DFS

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
- DFS có thể bị ảnh hưởng mạnh bởi thứ tự sinh hành động.
- Cần có cơ chế tránh lặp để hạn chế việc quay lại các trạng thái đã xét.

---

## 6.3. Uniform Cost Search - UCS

UCS là thuật toán tìm kiếm theo chi phí đồng nhất. Thay vì mở rộng node theo thứ tự được sinh ra như BFS, UCS luôn chọn node có **chi phí thấp nhất** trong frontier để mở rộng trước.

Trong đồ án, chi phí được xác định là **số ô bẩn còn lại trong trạng thái**. Vì vậy, UCS sẽ ưu tiên các trạng thái có ít ô bẩn hơn.

UCS vẫn thuộc nhóm **tìm kiếm không có thông tin**, vì thuật toán không sử dụng heuristic. Việc lựa chọn node chỉ dựa trên chi phí đã được định nghĩa trong bài toán.

### UCS Dạng 1

Ở dạng này, thuật toán lấy node có chi phí nhỏ nhất ra khỏi frontier trước, sau đó mới kiểm tra goal.

Quy trình chính:

1. Đưa trạng thái ban đầu vào frontier.
2. Chọn node có chi phí nhỏ nhất trong frontier.
3. Lấy node đó ra khỏi frontier.
4. Kiểm tra goal.
5. Nếu chưa đạt goal, sinh các trạng thái con.
6. Tính chi phí cho từng trạng thái con dựa trên số ô bẩn còn lại.
7. Thêm hoặc cập nhật trạng thái con vào frontier nếu có chi phí tốt hơn.
8. Lặp lại cho đến khi tìm được lời giải hoặc frontier rỗng.

### Nhận xét UCS

- UCS phù hợp với bài toán có chi phí giữa các trạng thái không đồng nhất.
- UCS ưu tiên mở rộng trạng thái có chi phí thấp hơn.
- Nếu chi phí được thiết kế phù hợp, UCS có thể tìm lời giải tối ưu theo tiêu chí chi phí.
- Trong bài toán này, tiêu chí chi phí là số ô bẩn còn lại, giúp thuật toán ưu tiên các trạng thái sạch hơn.
- UCS có thể tốn thời gian hơn BFS hoặc DFS do phải thường xuyên tìm node có chi phí nhỏ nhất trong frontier.
- Nếu cài đặt đơn giản bằng list, mỗi lần lấy node nhỏ nhất cần duyệt frontier. Nếu cài đặt tối ưu hơn, có thể dùng priority queue hoặc `heapq`.

---

## 6.4. Iterative Deepening Search - IDS

IDS là thuật toán tìm kiếm sâu dần. Thuật toán thực hiện DFS có giới hạn độ sâu nhiều lần, với giới hạn tăng dần từ `0`, `1`, `2`, ... cho đến khi tìm được goal.

IDS có thể được xem là sự kết hợp giữa BFS và DFS:

- Giống DFS ở chỗ sử dụng ít bộ nhớ do chỉ đi sâu trong một giới hạn nhất định.
- Giống BFS ở chỗ duyệt theo từng mức độ sâu tăng dần, nhờ đó có thể tìm được lời giải nông nhất nếu chi phí mỗi bước là như nhau.

Trong đồ án, IDS được xây dựng dựa trên hàm **Depth-Limited Search**.

### IDS Dạng 1

Ở dạng này, tại mỗi lần chạy Depth-Limited Search, thuật toán lấy node ra khỏi frontier trước, sau đó mới kiểm tra goal.

Quy trình chính:

1. Khởi tạo giới hạn độ sâu `limit = 0`.
2. Thực hiện Depth-Limited Search với giới hạn hiện tại.
3. Trong Depth-Limited Search, lấy node ra khỏi stack rồi kiểm tra goal.
4. Nếu tìm được goal, trả về lời giải.
5. Nếu gặp cutoff, tăng giới hạn độ sâu lên `1`.
6. Lặp lại cho đến khi tìm được lời giải hoặc xác định không còn trạng thái để mở rộng.

### IDS Dạng 2

Ở dạng này, tại mỗi lần chạy Depth-Limited Search, thuật toán kiểm tra goal ngay khi sinh trạng thái con.

Quy trình chính:

1. Kiểm tra riêng trạng thái ban đầu.
2. Khởi tạo giới hạn độ sâu `limit = 0`.
3. Thực hiện Depth-Limited Search với giới hạn hiện tại.
4. Sinh các trạng thái con trong phạm vi giới hạn độ sâu.
5. Nếu trạng thái con là goal, trả về lời giải ngay.
6. Nếu gặp cutoff, tăng giới hạn độ sâu lên `1`.
7. Lặp lại cho đến khi tìm được lời giải hoặc xác định không còn trạng thái để mở rộng.

### Nhận xét IDS

- IDS tiết kiệm bộ nhớ hơn BFS vì mỗi lần chỉ thực hiện tìm kiếm theo chiều sâu có giới hạn.
- IDS có khả năng tìm lời giải nông nhất khi mọi hành động có chi phí bằng nhau.
- IDS phù hợp khi không biết trước độ sâu của lời giải.
- IDS phải lặp lại việc duyệt các node ở độ sâu nhỏ nhiều lần, nên có thể tốn thời gian hơn DFS đơn thuần.
- Trong cài đặt IDS, không nên dùng `reached` toàn cục như BFS, vì thuật toán cần cho phép duyệt lại trạng thái ở các giới hạn độ sâu khác nhau. Thay vào đó, nên tránh vòng lặp trong cùng một đường đi hiện tại.

---

## 7. So sánh tổng quan các thuật toán

| Tiêu chí | BFS | DFS | UCS | IDS |
|---------|-----|-----|-----|-----|
| Nhóm thuật toán | Không có thông tin | Không có thông tin | Không có thông tin | Không có thông tin |
| Cấu trúc frontier | Queue | Stack | Priority Queue / List có chọn min | Stack trong từng lần DLS |
| Thứ tự mở rộng | Theo từng mức | Theo chiều sâu | Theo chi phí thấp nhất | Theo độ sâu tăng dần |
| Có dùng heuristic không? | Không | Không | Không | Không |
| Đầy đủ | Có, nếu không gian hữu hạn và tránh lặp | Không luôn đảm bảo nếu không kiểm soát độ sâu/lặp | Có, nếu chi phí hợp lệ và không gian được kiểm soát | Có, nếu không gian hữu hạn |
| Tối ưu | Có, nếu chi phí mỗi bước bằng nhau | Không | Có theo tiêu chí chi phí | Có theo số bước nếu chi phí mỗi bước bằng nhau |
| Bộ nhớ | Cao | Thấp hơn BFS | Có thể cao | Thấp hơn BFS |
| Phù hợp khi | Cần lời giải ít bước | Muốn cài đặt đơn giản, tiết kiệm bộ nhớ | Có tiêu chí chi phí rõ ràng | Không biết trước độ sâu lời giải |

---

## 8. So sánh Dạng 1 và Dạng 2

| Tiêu chí | Dạng 1 | Dạng 2 |
|---------|--------|--------|
| Thời điểm kiểm tra goal | Khi node được lấy ra khỏi frontier | Ngay khi sinh trạng thái con |
| Trạng thái ban đầu | Được kiểm tra trong vòng lặp | Được kiểm tra riêng trước vòng lặp |
| Khả năng dừng sớm | Có thể chậm hơn một chút | Có thể dừng sớm hơn khi child là goal |
| Ý nghĩa học thuật | Bám sát mô hình graph search truyền thống | Minh họa cách tối ưu thời điểm kiểm tra goal |
| Lưu ý khi cài đặt | Đơn giản, ít trường hợp đặc biệt | Cần xử lý riêng trạng thái ban đầu |

---

## 9. Cấu trúc thư mục hiện tại

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
│   ├── ucs.py
│   ├── ids.py
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
| `algorithms/ucs.py` | Cài đặt UCS Dạng 1 |
| `algorithms/ids.py` | Cài đặt IDS Dạng 1 và IDS Dạng 2 |
| `algorithms/algorithm_manager.py` | Quản lý danh sách thuật toán và điều phối hàm solve |
| `ui/vacuum_ui.py` | Xây dựng giao diện người dùng bằng Tkinter |

---

## 10. Giao diện chương trình

Giao diện được xây dựng bằng thư viện **Tkinter**.

Các chức năng hiện có:

- Nhập số dòng và số cột của ma trận.
- Tạo trạng thái ban đầu ngẫu nhiên.
- Chọn thuật toán BFS, DFS, UCS hoặc IDS.
- Chọn dạng giải: Dạng 1 hoặc Dạng 2.
- Điều chỉnh tốc độ chạy.
- Hiển thị từng bước di chuyển của máy hút bụi.
- Hiển thị trạng thái kết quả.
- Hiển thị process log trong quá trình giải.
- Dừng hoặc reset chương trình.

---

## 11. Hướng dẫn chạy chương trình

### 11.1. Yêu cầu môi trường

- Python 3.x
- Tkinter

Tkinter thường được cài sẵn cùng Python. Nếu chưa có, cần cài thêm theo hệ điều hành đang sử dụng.

### 11.2. Cách chạy

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

## 12. Kết quả hiện tại

Ở tiến độ hiện tại, đồ án đã hoàn thành các nội dung sau:

- Xây dựng được mô hình bài toán Vacuum Cleaner dưới dạng bài toán tìm kiếm.
- Cài đặt trạng thái ban đầu ngẫu nhiên theo ma trận `m x n`.
- Cài đặt điều kiện goal: không còn ô bẩn.
- Cài đặt hành động di chuyển máy hút bụi theo 4 hướng.
- Cài đặt BFS Dạng 1 và BFS Dạng 2.
- Cài đặt DFS Dạng 1 và DFS Dạng 2.
- Cài đặt UCS Dạng 1 với chi phí dựa trên số ô bẩn còn lại.
- Cài đặt IDS Dạng 1 và IDS Dạng 2 dựa trên Depth-Limited Search.
- Xây dựng giao diện Tkinter để trực quan hóa quá trình giải.
- Hiển thị số bước, thời gian thực thi và log quá trình tìm kiếm.

---

## 13. Hạn chế hiện tại

Do đồ án đang trong quá trình phát triển, chương trình hiện còn một số hạn chế:

- Các thuật toán hiện tại mới thuộc nhóm tìm kiếm không có thông tin, chưa mở rộng sang nhóm tìm kiếm có thông tin.
- Chưa cài đặt các thuật toán sử dụng heuristic như Greedy Best-First Search hoặc A*.
- Chưa có biểu đồ so sánh hiệu suất giữa các thuật toán.
- Chưa lưu kết quả chạy ra file.
- Với ma trận lớn, không gian trạng thái tăng nhanh khiến thời gian chạy và bộ nhớ sử dụng có thể tăng đáng kể.
- UCS có thể tốn thêm chi phí xử lý do cần chọn node có chi phí nhỏ nhất trong frontier.
- IDS có thể duyệt lại một số trạng thái nhiều lần do đặc trưng tăng dần giới hạn độ sâu.
- Nút Stop hiện chủ yếu dừng quá trình hiển thị, chưa can thiệp sâu vào thuật toán nếu thuật toán đang chạy lâu.

---

## 14. Hướng phát triển

Trong các giai đoạn tiếp theo, đồ án có thể mở rộng theo các hướng:

- Bổ sung các thuật toán tìm kiếm có thông tin như Greedy Best-First Search và A*.
- Thiết kế heuristic phù hợp cho bài toán Vacuum Cleaner, ví dụ số ô bẩn còn lại, khoảng cách đến ô bẩn gần nhất hoặc tổng khoảng cách đến các ô bẩn.
- Bổ sung thống kê số trạng thái đã duyệt.
- Vẽ biểu đồ so sánh thời gian chạy, số bước, chi phí và bộ nhớ.
- Cải thiện giao diện để chạy mượt hơn với ma trận lớn.
- Cho phép người dùng tự thiết lập trạng thái ban đầu thay vì chỉ random.
- Lưu log hoặc kết quả thực nghiệm ra file.
- Bổ sung chế độ so sánh nhiều thuật toán trên cùng một trạng thái ban đầu.

---

## 15. Kết luận

Đồ án đã xây dựng được phần nền tảng của một bài toán tìm kiếm trong Trí tuệ nhân tạo thông qua mô hình **Vacuum Cleaner Problem**. Chương trình thể hiện rõ các thành phần quan trọng của một bài toán tìm kiếm, bao gồm không gian trạng thái, trạng thái ban đầu, trạng thái đích, hành động, chi phí và lời giải.

Ở giai đoạn hiện tại, bốn thuật toán BFS, DFS, UCS và IDS được sử dụng để minh họa nhóm **tìm kiếm không có thông tin**. Mỗi thuật toán có chiến lược mở rộng trạng thái khác nhau: BFS mở rộng theo từng mức, DFS mở rộng theo chiều sâu, UCS mở rộng theo chi phí thấp nhất, còn IDS thực hiện tìm kiếm sâu dần theo giới hạn độ sâu.

Việc cài đặt mỗi thuật toán theo hai dạng kiểm tra goal giúp làm rõ ảnh hưởng của thời điểm kiểm tra trạng thái đích đến quá trình tìm kiếm. Đây là cơ sở quan trọng để tiếp tục mở rộng đồ án sang các thuật toán tìm kiếm có thông tin như Greedy Best-First Search và A* trong các giai đoạn tiếp theo.

---

## 16. Tài liệu tham khảo

1. Russell, S., & Norvig, P. (2016). *Artificial Intelligence: A Modern Approach* (3rd ed.). Pearson.
2. GeeksforGeeks. (n.d.). Breadth First Search or BFS for a Graph.
3. GeeksforGeeks. (n.d.). Depth First Search or DFS for a Graph.
4. GeeksforGeeks. (n.d.). Uniform Cost Search.
5. GeeksforGeeks. (n.d.). Iterative Deepening Search.
6. Python Software Foundation. (n.d.). Tkinter — Python interface to Tcl/Tk.

---

## 👨‍💻 Tác giả

**Họ và tên:** Nguyễn Lê Huy  
**MSSV:** 24110221  
**Môn học:** Trí Tuệ Nhân Tạo  
**Giảng viên hướng dẫn:** Phan Thị Huyền Trang
