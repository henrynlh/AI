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

### 3.4. Tìm kiếm trong môi trường phức tạp: NO OBSERVATION SEARCH, PARTIAL OBSERVATION SEARCH, AND-OR-GRAPH SEARCH

Tìm kiếm trong môi trường phức tạp là nhóm thuật toán được sử dụng khi tác nhân không biết đầy đủ hoặc không quan sát chính xác toàn bộ trạng thái của môi trường. Thay vì chỉ xử lý một trạng thái duy nhất, thuật toán sẽ làm việc với một tập các trạng thái có thể xảy ra, gọi là trạng thái niềm tin hay belief state.

Trong bài toán máy hút bụi, môi trường phức tạp được mô phỏng bằng cách cho tác nhân không biết chắc chắn toàn bộ vị trí các ô sạch, ô bẩn hoặc chỉ nhìn thấy một phần môi trường. Khi đó, thuật toán phải đồng thời xử lý nhiều trạng thái có thể xảy ra và tìm ra chuỗi hành động giúp tất cả các trạng thái đó đạt đến mục tiêu.

Các thuật toán tiêu biểu:

- **No Observation Search**
- **Partial Observation Search**
- **AND-OR-GRAPH Search**

Đặc điểm chính:

- Phù hợp với môi trường không chắc chắn hoặc không quan sát đầy đủ.
- Thuật toán xử lý trên belief state thay vì một trạng thái đơn.
- Một hành động chung được áp dụng đồng thời cho nhiều trạng thái có thể xảy ra.
- Nếu một trạng thái thực hiện được hành động thì trạng thái đó sẽ di chuyển theo hành động tương ứng.
- Nếu một trạng thái không thực hiện được hành động thì trạng thái đó giữ nguyên.
- Nếu một trạng thái đã đạt mục tiêu thì trạng thái đó dừng lại và chờ các trạng thái còn lại tiếp tục xử lý.
- Thuật toán chỉ kết thúc khi tất cả các trạng thái trong belief state đều đạt trạng thái đích.


#### Giao diện minh họa

| Nhóm thuật toán | Giao diện |
|----------------|-----------|
| **NO OBSERVATION SEARCH** | <img src="images/no_observation_search.gif" width="700" alt="NO OBSERVATION SEARCH"> |
| **PARTIAL OBSERVATION SEARCH** | <img src="images/partial_observation_search.gif" width="700" alt="PARTIAL OBSERVATION SEARCH"> |
| **AND-OR-GRAPH SEARCH** | <img src="images/and_or_graph_search.gif" width="700" alt="AND-OR-GRAPH SEARCH"> |

## 3.5. Các thuật toán tìm kiếm ràng buộc: BACKTRACKING, FORWARD CHECKING, AC-3, MIN CONFLICTS

Tìm kiếm ràng buộc là nhóm thuật toán được sử dụng cho các bài toán cần gán giá trị cho nhiều biến sao cho thỏa mãn một tập các điều kiện cho trước. Thay vì chỉ tìm đường đi từ trạng thái đầu đến trạng thái đích, thuật toán tập trung vào việc xây dựng một phép gán hợp lệ cho toàn bộ bài toán.

Trong bài toán tô màu bản đồ, mỗi vùng trên bản đồ được xem là một biến cần được gán màu. Mục tiêu là tô màu toàn bộ bản đồ sao cho hai vùng kề nhau không được có cùng màu. Các màu được sử dụng trong chương trình gồm: Đỏ, Vàng, Xanh lá và Xanh dương.

Các thuật toán tiêu biểu:

- **Backtracking**
- **Forward Checking**
- **AC-3**
- **Min Conflicts**

Đặc điểm chính:

- Phù hợp với các bài toán có nhiều biến và nhiều ràng buộc.
- Thuật toán làm việc trên tập các phép gán màu cho từng vùng trên bản đồ.
- Mỗi hành động tương ứng với việc chọn một vùng chưa tô và gán cho vùng đó một màu.
- Sau mỗi lần gán màu, thuật toán kiểm tra xem màu vừa chọn có vi phạm ràng buộc với các vùng kề hay không.
- Thuật toán chỉ kết thúc khi tất cả các vùng trên bản đồ đều được tô màu và không có hai vùng kề nhau nào bị trùng màu.

#### Giao diện minh họa

| Nhóm thuật toán | Giao diện |
|----------------|-----------|
| **BACKTRACKING** | <img src="images/backtracking.gif" width="650" alt="BACKTRACKING"> |
| **FORWARD CHECKING** | <img src="images/forward_checking.gif" width="650" alt="FORWARD CHECKING"> |
| **AC-3** | <img src="images/ac_3.gif" width="650" alt="AC-3"> |
| **MIN CONFLICTS** | <img src="images/min_conflicts.gif" width="650" alt="MIN CONFLICTS"> |

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

