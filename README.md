# 🎮 Đồ án: Trò chơi Đoán chữ - Wordle (Phiên bản 6 Chữ cái)

Đồ án môn **Cấu trúc Dữ liệu và Thuật toán (DSA)**: Tái hiện game Wordle với **6 chữ cái** và **8 lượt đoán**, hỗ trợ cả CLI và GUI.

---

## 🌟 Tính năng
- **Từ điển phân cấp**: ~30,000 từ tiếng Anh chia 3 độ khó (Dễ/Trung Bình/Khó) dựa trên tần suất.
- **Giao diện đa dạng**: GUI Dark Mode (`customtkinter`) thiết kế hiện đại, nhiều hoạt ảnh (animation), và chế độ CLI nguyên bản trên Terminal.

---

## 🧠 Áp dụng DSA

1. **`Set` (Hash Table) cho Từ điển**:
   - Lưu trữ hơn 30,000 từ, tiêu tốn chỉ **~7.3 MB RAM**.
   - Tra cứu từ hợp lệ với độ phức tạp **$\mathcal{O}(1)$**, tối ưu vượt trội so với tìm kiếm trong mảng thông thường.

2. **Thuật toán vòng lặp 2 bước (Two-pass Array Iteration)**:
   - Xử lý chính xác các trường hợp trùng chữ cái (ví dụ: đoán thiếu/thừa từ có 2 chữ P), tránh gán sai màu Xanh lá/Vàng.
   - Duyệt vòng 1 để tìm khớp 100% (Exact Match) và vòng 2 để tìm khớp lệch (Partial Match). Độ phức tạp **$\mathcal{O}(L)$** (với $L=6$ là độ dài từ).

---

## 🚀 Cài đặt & Sử dụng

Yêu cầu: **Python 3.9+**

```bash
# Cài đặt thư viện yêu cầu (dùng cho GUI)
pip install -r requirements.txt

# Chạy bản đồ họa (GUI)
python gui.py

# Hoặc chạy bản dòng lệnh (CLI)
python main.py
```

---

## 📂 Tổ chức mã nguồn
*   `gui.py` / `main.py`: File khởi chạy tương ứng cho GUI và CLI.
*   `game.py`: Core logic (bộ chấm điểm, quản lý trạng thái, vòng chơi).
*   `ui.py`: Vẽ giao diện màu cho phiên bản Terminal.
*   `word_manager.py` / `categorize.py`: Script đọc, phân loại và quản lý từ điển.
*   `words_*.txt`: Tập dữ liệu từ vựng cục bộ.