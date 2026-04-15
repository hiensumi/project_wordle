#  Đồ án: Trò chơi Đoán chữ - Wordle (Đa Ngôn Ngữ)

Đồ án môn **Cấu trúc Dữ liệu và Thuật toán (DSA)**: Tái hiện game Wordle với **phiên bản Tiếng Anh (6 chữ cái)** và **phiên bản Tiếng Việt (1 Tiếng - Blind Length)**.

---

##  Tính năng Nổi bật
- **Chế độ Ngoại Ngữ đa dạng**: 
  - **Tiếng Anh**: Đoán từ 6 chữ cái, phân thành 3 cấp độ (Dễ/Trung Bình/Khó) từ bộ 30,000 từ.
  - **Tiếng Việt (1 Tiếng)**: Chế độ "Độ dài ẩn" (Blind length) cực độc đáo. Đoán từ 1 âm tiết (tối đa 7 ký tự). Không giới hạn độ dài từ nhập vào phải bằng từ gốc.
- **Bàn phím Ảo Thuần Việt**: 
  - Bàn phím được thiết kế lại riêng cho Tiếng Việt (loại bỏ W, F, J, Z).
  - Có hàng phím nguyên âm mở rộng (`Ă, Â, Đ, Ê, Ô, Ơ, Ư`) và 5 phím Dấu riêng biệt để hỗ trợ gõ Telex trực tiếp trên giao diện bằng chuột.
  - Tích hợp bộ gõ **bogo** xử lý phím bấm vật lý thời gian thực.
- **Giao diện hiện đại**: GUI Dark Mode (`customtkinter`) với hiệu ứng lật mở màu sắc mượt mà, viền bo tròn tinh tế bắt sáng bàn phím.

---

##  Áp dụng DSA & Cấu trúc Dữ liệu

1. **`Set` (Hash Table) thay vì `B-Tree` cho Từ điển**:
   - Dữ liệu từ vựng (~30,000 từ Tiếng Anh, 6,256 từ Tiếng Việt) được nạp vào memory dưới dạng Hash Set.
   - **Phân tích độ phức tạp**: Tra cứu từ mất $\mathcal{O}(1)$. Memory tiêu tốn chỉ **~7 MB RAM**, tối ưu vượt trội so với sử dụng Cây B-Tree (chiếm >100MB Memory do tính chất lưu trữ Object/Pointer của Python) cho bài toán chỉ mang tính chất Read-only này.

2. **Thuật toán Đánh giá Lệch độ dài (Blind Length - Two-pass Array)**:
   - Xử lý các trường hợp từ nhập vào dài hơn hoặc ngắn hơn từ đích (ví dụ: đích "NGHIÊNG", nhập "THƯƠNG").
   - Duyệt vòng 1 bằng vòng lặp giới hạn `min(len(guess), len(answer))` để tìm khớp 100% (Xanh lá).
   - Duyệt vòng 2 xử lý Partial Match (Màu vàng) kết hợp với từ điển tần suất chữ cái, giúp không bị gán dư màu vàng khi từ bị trùng lặp chữ. Độ phức tạp duy trì ở ngưỡng an toàn $\mathcal{O}(L)$.

---

##  Cài đặt & Sử dụng

Yêu cầu môi trường: **Python 3.9+**

```bash
# Cài đặt thư viện yêu cầu (gui và gõ tiếng Việt)
pip install customtkinter bogo

# Chạy bản đồ họa (GUI)
python gui.py

# Hoặc chạy bản dòng lệnh (CLI - Tiếng Anh)
python main.py
```

---

##  Tổ chức Mã nguồn
*   `gui.py`: Giao diện chính (CTk), tích hợp xử lý bàn phím vật lý/ảo và buffer Telex.
*   `game.py`: Core logic chấm điểm mảng hai lớp, quản lý biến trạng thái (hỗ trợ mismatched length).
*   `word_manager.py`: Script đọc, phân loại cấp độ, và xử lý chuyển đổi giữa tập `vn_words` / `en_words`.
*   `bogo_demo.py` / `fetch_vn_words.py`: Các script phụ trợ tải và demo xử lý tiếng Việt.
*   `words_*.txt`: Tập dữ liệu chuẩn hóa, lọc nhiễu âm tiết.

---

##  Tuyên bố Bản quyền & Tham khảo (Citations)

Dự án này sử dụng một số thư viện mã nguồn mở có sẵn. Theo đúng quy định của đề bài đồ án, toàn bộ thuật toán liên quan đến CTDL & TT (ví dụ: HashSet, Two-pass Array Match) đều được sinh viên triển khai toàn bộ từ đầu.

**Các thư viện UI và mã dựng sẵn đã sử dụng:**
1. **`customtkinter`**: Thư viện hỗ trợ vẽ giao diện đồ hoạ hiện đại (Win32/Tkinter) cho Python. [Link GitHub](https://github.com/TomSchimansky/CustomTkinter)
2. **`bogo`**: Thư viện xử lý chuỗi Telex siêu tốc phục vụ bộ máy nhập liệu Tiếng Việt theo thời gian thực tại `gui.py`. Tác giả: Trung Ngo. [Link GitHub](https://github.com/BoGoEngine/bogo-python)
3. **Từ điển dữ liệu**: 
   - Tiếng Anh: Tham khảo Wordle Dictionary cơ bản.
   - Tiếng Việt: Trích xuất xử lý từ `vinlp` và các Github Gists từ điển thông dụng, lọc tay lại bằng regex cho ra `words_vn.txt`.
