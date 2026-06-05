# 🤖 Học phần: Trí tuệ nhân tạo

## 1. Giới thiệu học phần

**Trí tuệ nhân tạo** là học phần cung cấp các kiến thức nền tảng về cách xây dựng hệ thống có khả năng suy luận, tìm kiếm lời giải, ra quyết định và học từ môi trường.

Trong học phần này, sinh viên được tiếp cận các bài toán cơ bản của AI thông qua việc mô hình hóa bài toán, xây dựng không gian trạng thái, xác định trạng thái ban đầu, trạng thái đích, hành động, chi phí và lời giải. Từ đó, sinh viên có thể cài đặt, mô phỏng và đánh giá cách hoạt động của nhiều nhóm thuật toán khác nhau trong Trí tuệ nhân tạo.

Các nội dung chính của học phần gồm:

- Tìm kiếm không có thông tin.
- Tìm kiếm có thông tin.
- Tìm kiếm cục bộ.
- Tìm kiếm trong môi trường phức tạp.
- Bài toán thỏa mãn ràng buộc.
- Học tăng cường.

Thông qua các bài thực hành và đồ án, sinh viên không chỉ nắm được lý thuyết mà còn hiểu cách áp dụng thuật toán AI vào những bài toán cụ thể.

---

## 2. Mục tiêu học phần

Học phần hướng đến các mục tiêu chính sau:

- Hiểu được khái niệm cơ bản về Trí tuệ nhân tạo và vai trò của AI trong khoa học máy tính.
- Biết cách biểu diễn một bài toán AI dưới dạng không gian trạng thái.
- Xác định được trạng thái ban đầu, trạng thái đích, hành động, chi phí và lời giải của một bài toán tìm kiếm.
- Cài đặt được các thuật toán tìm kiếm cơ bản bằng ngôn ngữ lập trình (Python).
- Phân biệt được tìm kiếm không có thông tin và tìm kiếm có thông tin.
- Hiểu được vai trò của heuristic trong các thuật toán như Greedy, A\* và IDA\*.
- So sánh được ưu điểm, hạn chế và phạm vi áp dụng của từng nhóm thuật toán.
- Làm quen với các bài toán tối ưu cục bộ, bài toán ràng buộc và học tăng cường.
- Rèn luyện kỹ năng phân tích thuật toán, xây dựng chương trình mô phỏng và trực quan hóa quá trình giải.

---

## 3. Các thuật toán được học

### 3.1. Tìm kiếm không có thông tin

Tìm kiếm không có thông tin là nhóm thuật toán không sử dụng tri thức bổ sung về khoảng cách hoặc mức độ gần với trạng thái đích. Thuật toán chỉ dựa vào cấu trúc không gian trạng thái để mở rộng các node.

Các thuật toán tiêu biểu:

- **BFS** - Breadth-First Search
- **DFS** - Depth-First Search
- **UCS** - Uniform Cost Search
- **IDS** - Iterative Deepening Search

Đặc điểm chính:

- **BFS** mở rộng node theo từng mức, phù hợp khi cần tìm lời giải có số bước ngắn nhất với chi phí các bước bằng nhau.
- **DFS** mở rộng sâu theo từng nhánh, tiết kiệm bộ nhớ hơn BFS nhưng có thể đi sâu vào nhánh không phù hợp.
- **UCS** chọn node có chi phí đường đi nhỏ nhất, phù hợp với bài toán có chi phí hành động khác nhau.
- **IDS** kết hợp ưu điểm của DFS và BFS bằng cách tăng dần giới hạn độ sâu.

#### Giao diện minh họa

| Nhóm thuật toán | Giao diện |
|----------------|-----------|
| **BFS_Dạng 1** | <img src="images/bfs_d1.gif" width="700" alt="BFS DẠNG 1"> |
| **BFS_Dạng 2** | <img src="images/bfs_d2.gif" width="700" alt="BFS DẠNG 2"> |
| **DFS_Dạng 1** | <img src="images/dfs_d1.gif" width="700" alt="DFS DẠNG 1"> |
| **DFS_Dạng 2** | <img src="images/dfs_d2.gif" width="700" alt="DFS DẠNG 2"> |
| **IDS_Dạng 1** | <img src="images/ids_d1.gif" width="700" alt="IDS DẠNG 1"> |
| **IDS_Dạng 2** | <img src="images/ids_d2.gif" width="700" alt="IDS DẠNG 2"> |
| **UCS_Dạng 1** | <img src="images/ucs_d1.gif" width="700" alt="UCS DẠNG 1"> |

---

### 3.2. Tìm kiếm có thông tin

Tìm kiếm có thông tin sử dụng thêm hàm heuristic để đánh giá trạng thái và ưu tiên mở rộng những trạng thái có khả năng dẫn đến lời giải tốt hơn.

Các thuật toán tiêu biểu:

- **Greedy Best-First Search**
- **A\***
- **IDA\***

Đặc điểm chính:

- **Greedy Best-First Search** chọn node có heuristic nhỏ nhất, tức là node có vẻ gần trạng thái đích nhất tại thời điểm xét.
- **A\*** kết hợp chi phí thực tế đã đi và chi phí ước lượng đến đích.
- **IDA\*** kết hợp ý tưởng của A\* và IDS, phù hợp khi muốn giảm bộ nhớ sử dụng.

#### Giao diện minh họa

| Nhóm thuật toán | Giao diện |
|----------------|-----------|
| **GREEDY** | <img src="images/greedy.gif" width="700" alt="GREEDY"> |
| **A\*** | <img src="images/astar.gif" width="700" alt="ASTAR"> |
| **IDA\*** | <img src="images/idastar.gif" width="700" alt="IDASTAR"> |

---

### 3.3. Tìm kiếm cục bộ

Tìm kiếm cục bộ là nhóm thuật toán tập trung cải thiện trạng thái hiện tại thay vì lưu toàn bộ cây tìm kiếm. Nhóm thuật toán này thường được dùng trong các bài toán tối ưu có không gian trạng thái lớn.

Các thuật toán tiêu biểu:

- **Simple Hill Climbing**
- **Steepest Ascent Hill Climbing**
- **Stochastic Hill Climbing**
- **Random Restart Hill Climbing**
- **Local Beam Search**
- **Simulated Annealing**

Đặc điểm chính:

- Phù hợp với các bài toán tối ưu.
- Không nhất thiết lưu toàn bộ đường đi từ trạng thái ban đầu.
- Có thể gặp cực trị cục bộ nếu không có cơ chế thoát khỏi trạng thái kẹt.

#### Giao diện minh họa

| Nhóm thuật toán | Giao diện |
|----------------|-----------|
| **SIMPLE HILL CLIMBING** | <img src="images/simple_hill_climbing.gif" width="700" alt="SIMPLE HILL CLIMBING"> |
| **STEEPEST ASCENT HILL CLIMBING** | <img src="images/steepest_ascent_hill_climbing.gif" width="700" alt="STEEPEST ASCENT HILL CLIMBING"> |
| **STOCHASTIC HILL CLIMBING** | <img src="images/stochastic_hill_climbing.gif" width="700" alt="STOCHASTIC HILL CLIMBING"> |
| **RANDOM RESTART HILL CLIMBING** | <img src="images/random_restart_hill_climbing.gif" width="700" alt="RANDOM RESTART HILL CLIMBING"> |
| **LOCAL BEAM SEARCH** | <img src="images/local_beam_search.gif" width="700" alt="LOCAL BEAM SEARCH"> |
| **SIMULATED ANNEALING** | <img src="images/simulated_annealing.gif" width="700" alt="SIMULATED ANNEALING"> |

---

## 4. Tài liệu tham khảo

1. Russell, S., & Norvig, P. (2016). *Artificial Intelligence: A Modern Approach* (3rd ed.). Pearson.
2. Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
3. GeeksforGeeks. *Artificial Intelligence Algorithms*.
4. Tài liệu bài giảng học phần Trí tuệ nhân tạo.

---

## 5. Thông tin tác giả

**Họ và tên:** Nguyễn Lê Huy  
**MSSV:** 24110221  
**Môn học:** Trí tuệ nhân tạo  
**Giảng viên hướng dẫn:** Phan Thị Huyền Trang  

---

