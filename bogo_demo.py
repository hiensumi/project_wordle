import customtkinter as ctk
import bogo

class VietnameseWordleDemo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Demo Gõ Tiếng Việt - Wordle")
        self.geometry("400x300")
        
        # Biến ẩn lưu trữ toàn bộ lịch sử gõ phím nguyên bản (VD: "truongf")
        self.hidden_buffer = ""
        
        # Tiêu đề
        self.title_label = ctk.CTkLabel(self, text="Nhập liệu Telex 6 ô", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)
        
        # Khu vực 6 ô chữ (Wordle Board)
        self.board_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.pack(pady=10)
        
        self.cells = []
        for i in range(6):
            cell = ctk.CTkLabel(
                self.board_frame, text="", width=40, height=50, 
                fg_color="#3a3a3c", text_color="white", font=("Arial", 24, "bold"),
                corner_radius=5
            )
            cell.grid(row=0, column=i, padx=5)
            self.cells.append(cell)
            
        # Label hiển thị Log quá trình
        self.log_label = ctk.CTkLabel(self, text="Buffer: ''", font=("Arial", 14), text_color="gray")
        self.log_label.pack(pady=20)
        
        # Nhận sự kiện Gõ phím
        self.bind("<Key>", self.handle_keypress)
        # Nhập Backspace xóa chữ
        self.bind("<BackSpace>", self.handle_backspace)
        # focus
        self.focus_set()

    def update_board(self):
        # 1. Dùng bogo để dịch chuỗi gõ thuần (Telex) thành chữ Tiếng Việt có dấu
        vietnamese_text = bogo.process_sequence(self.hidden_buffer).upper()
        
        # 2. Xóa sạch 6 ô cũ
        for cell in self.cells:
            cell.configure(text="")
            
        # 3. Điền chữ Tiếng Việt mới vào các ô, KHÔNG được vượt quá 6 ô
        # (Nếu gõ dài hơn 6 ô thì ta chỉ điền 6 ký tự đầu, hoặc chặn ở hàm gõ)
        display_text = vietnamese_text[:6] 
        
        for i, char in enumerate(display_text):
            self.cells[i].configure(text=char)
            
        # 4. Hiển thị Log cho dễ hiểu debug
        self.log_label.configure(text=f"Buffer (Nguyên bản): '{self.hidden_buffer}'\n"
                                      f"Bogo dịch ra: '{vietnamese_text}'\n"
                                      f"Số ô đã điền: {len(display_text)}/6")

    def handle_keypress(self, event):
        # Chỉ nhận chữ cái A-Z và Phím cách (Space)
        if event.char.isalpha() or event.keysym == 'space':
            char = event.char.lower() if event.char.isalpha() else ' '
            
            # Dự đoán trước xem nếu thêm phím này thì bogo dịch ra dài bao nhiêu ký tự
            test_buffer = self.hidden_buffer + char
            test_vietnamese = bogo.process_sequence(test_buffer)
            
            # Chỉ cho phép gõ thêm nếu văn bản sau khi dịch có độ dài NHỎ HƠN HOẶC BẰNG 6
            # Điều này giúp chặn đúng lúc, nhưng vẫn cho gõ thêm dấu (VD: "truong" (6) + "f" -> "trường" (6))
            if len(test_vietnamese) <= 6:
                self.hidden_buffer += char
                self.update_board()

    def handle_backspace(self, event):
        # Xóa phím gõ cuối cùng trong buffer ẩn
        if len(self.hidden_buffer) > 0:
            self.hidden_buffer = self.hidden_buffer[:-1]
            self.update_board()

if __name__ == "__main__":
    app = VietnameseWordleDemo()
    app.mainloop()
