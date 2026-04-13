import customtkinter as ctk
from tkinter import messagebox
import os
from word_manager import WordManager
from game import Game

# Khởi tạo chủ đề mặc định
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Cấu hình màu sắc giao diện theo bảng màu gốc của Wordle
BG_COLOR = "#121213"
TEXT_COLOR = "#ffffff"
CORRECT_COLOR = "#538d4e"
PRESENT_COLOR = "#b59f3b"
ABSENT_COLOR = "#3a3a3c"
BORDER_COLOR = "#3a3a3c"
KEY_BG = "#818384"

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle DSA Visual")
        self.root.geometry("550x750")
        self.root.configure(fg_color=BG_COLOR)
        self.root.resizable(False, False)
        
        # Load quản lý từ vựng
        base_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            self.manager = WordManager(base_dir)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải từ điển: {e}")
            self.root.destroy()
            return
            
        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        """Màn hình chọn cấp độ đầu tiên bằng GUI"""
        self.setup_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.setup_frame.pack(expand=True, fill='both')
        
        ctk.CTkLabel(self.setup_frame, text="WORDLE 6+", font=("Helvetica", 42, "bold"), text_color=TEXT_COLOR).pack(pady=(120, 20))
        ctk.CTkLabel(self.setup_frame, text="Đồ án môn DSA (Cấu trúc dữ liệu)", font=("Helvetica", 14), text_color=KEY_BG).pack(pady=(0, 40))
        
        ctk.CTkLabel(self.setup_frame, text="Vui lòng chọn độ khó:", font=("Helvetica", 16, "bold"), text_color=TEXT_COLOR).pack(pady=10)
        
        ctk.CTkButton(self.setup_frame, text="Dễ (Easy)", font=("Helvetica", 14, "bold"), fg_color=CORRECT_COLOR, hover_color="#43723e", 
                      text_color=TEXT_COLOR, command=lambda: self.start_game('easy'), height=45, width=200).pack(pady=10)
                  
        ctk.CTkButton(self.setup_frame, text="Trung bình (Medium)", font=("Helvetica", 14, "bold"), fg_color=PRESENT_COLOR, hover_color="#968331", 
                      text_color=TEXT_COLOR, command=lambda: self.start_game('medium'), height=45, width=200).pack(pady=10)
                  
        ctk.CTkButton(self.setup_frame, text="Khó (Hard)", font=("Helvetica", 14, "bold"), fg_color=ABSENT_COLOR, hover_color="#2b2b2d", 
                      text_color=TEXT_COLOR, command=lambda: self.start_game('hard'), height=45, width=200).pack(pady=10)

    def start_game(self, difficulty):
        """Khởi tạo Board cho Game sau khi chọn độ khó"""
        self.setup_frame.destroy()
        
        self.answer = self.manager.get_random_word(difficulty)
        self.game = Game(self.answer, max_guesses=8)
        
        self.current_guess = ""
        self.current_row = 0
        
        self.build_ui()
        self.root.bind("<Key>", self.handle_keypress)
        
    def build_ui(self):
        """Xây dựng khung lưới bảng chơi và bàn phím"""
        ctk.CTkLabel(self.root, text="WORDLE", font=("Helvetica", 28, "bold"), text_color=TEXT_COLOR).pack(pady=(20, 10))
        
        # Grid chữ cái
        self.grid_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.grid_frame.pack(pady=10)
        
        self.labels = []
        for i in range(8):
            row_labels = []
            for j in range(6):
                # Tạo các ô label (CTkButton không bấm được để làm ô hiện text đẹp hơn CTkLabel)
                lbl = ctk.CTkLabel(self.grid_frame, text="", font=("Helvetica", 24, "bold"), text_color=TEXT_COLOR, 
                                   width=50, height=50, fg_color=BG_COLOR)
                lbl.grid(row=i, column=j, padx=4, pady=4)
                
                # Để border bo góc đẹp, ta dùng một CTkFrame nhỏ bọc ngoài (hack nhẹ ở CTk)
                # Tuy nhiên ở đây tối ưu nhất là thay label.configure
                row_labels.append(lbl)
            self.labels.append(row_labels)
            
        # Keyboard ảo dưới đáy màn hình
        self.keyboard_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.keyboard_frame.pack(pady=30)
        
        self.keys = {}
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for r_idx, row in enumerate(rows):
            row_frame = ctk.CTkFrame(self.keyboard_frame, fg_color=BG_COLOR)
            row_frame.pack(pady=3)
            
            if r_idx == 2:
                btn = ctk.CTkButton(row_frame, text="ENTER", font=("Helvetica", 12, "bold"), fg_color=KEY_BG, text_color=TEXT_COLOR, 
                                    command=self.submit_guess, width=65, height=45, hover_color="#6c6e6f")
                btn.pack(side="left", padx=3)
                
            for char in row:
                btn = ctk.CTkButton(row_frame, text=char, font=("Helvetica", 14, "bold"), fg_color=KEY_BG, text_color=TEXT_COLOR, 
                                    width=40, height=45, command=lambda c=char: self.type_char(c), hover_color="#6c6e6f")
                btn.pack(side="left", padx=2)
                self.keys[char] = btn
                
            if r_idx == 2:
                btn = ctk.CTkButton(row_frame, text="⌫", font=("Helvetica", 16), fg_color=KEY_BG, text_color=TEXT_COLOR, 
                                    command=self.delete_char, width=50, height=45, hover_color="#6c6e6f")
                btn.pack(side="left", padx=3)

    def handle_keypress(self, event):
        """Xử lý sự kiện khi gõ bàn phím vật lý"""
        if self.game.is_over: return
        
        char = event.keysym.upper()
        if char.isalpha() and len(char) == 1:
            self.type_char(char)
        elif event.keysym == "BackSpace":
            self.delete_char()
        elif event.keysym == "Return":
            self.submit_guess()

    def type_char(self, char):
        if self.game.is_over: return
        if len(self.current_guess) < 6:
            self.current_guess += char
            self.update_current_row()

    def delete_char(self):
        if self.game.is_over: return
        if len(self.current_guess) > 0:
            self.current_guess = self.current_guess[:-1]
            self.update_current_row()

    def update_current_row(self):
        for i in range(6):
            if i < len(self.current_guess):
                self.labels[self.current_row][i].configure(text=self.current_guess[i], fg_color="#3a3a3c")
            else:
                self.labels[self.current_row][i].configure(text="", fg_color=BG_COLOR)

    def submit_guess(self):
        if self.game.is_over: return
        
        if len(self.current_guess) != 6:
            messagebox.showwarning("Thiếu ký tự", "Từ bạn nhập phải có đủ 6 chữ cái!")
            return
            
        if not self.manager.is_valid(self.current_guess):
            messagebox.showwarning("Không hợp lệ", f"'{self.current_guess}' không có trong từ điển tiếng Anh!")
            return
            
        # Nạp từ vào logic game
        eval_result = self.game.make_guess(self.current_guess)
        
        # Mở màu trên lưới Grid
        for i, (char, status) in enumerate(eval_result):
            color = BG_COLOR
            if status == Game.CORRECT:
                color = CORRECT_COLOR
            elif status == Game.PRESENT:
                color = PRESENT_COLOR
            else:
                color = ABSENT_COLOR
                
            self.labels[self.current_row][i].configure(fg_color=color, text_color=TEXT_COLOR, corner_radius=6)
            
        # Cập nhật màu lên bàn phím ảo
        for char, status in self.game.letter_status.items():
            if char in self.keys:
                current_bg = self.keys[char].cget("fg_color")
                if status == Game.CORRECT:
                    self.keys[char].configure(fg_color=CORRECT_COLOR, hover_color=CORRECT_COLOR)
                elif status == Game.PRESENT and current_bg != CORRECT_COLOR:
                    self.keys[char].configure(fg_color=PRESENT_COLOR, hover_color=PRESENT_COLOR)
                elif status == Game.ABSENT and current_bg not in [CORRECT_COLOR, PRESENT_COLOR]:
                    self.keys[char].configure(fg_color=ABSENT_COLOR, hover_color=ABSENT_COLOR)

        self.current_row += 1
        self.current_guess = ""
        
        if self.game.is_won:
            self.show_end_game_msg("✨ CHIẾN THẮNG ✨", f"Chúc mừng! Bạn đã đoán đúng từ \n'{self.game.answer}'\nsau {self.current_row} lượt.")
        elif self.game.is_over:
            self.show_end_game_msg("❌ THUA CUỘC ❌", f"Bạn đã hết lượt chơi.\nTừ chính xác là: '{self.game.answer}'")

    def show_end_game_msg(self, title, message):
        """Hộp thoại cuối màn chơi"""
        response = messagebox.askyesno(title, f"{message}\n\nBạn có muốn chơi ván mới không?")
        if response:
            self.root.destroy()
            new_root = ctk.CTk()
            app = WordleGUI(new_root)
            new_root.mainloop()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = WordleGUI(root)
    root.mainloop()
