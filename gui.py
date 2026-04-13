import tkinter as tk
from tkinter import messagebox
import os
from word_manager import WordManager
from game import Game

# Cấu hình màu sắc giao diện theo bảng màu gốc của Wordle (Dark Theme)
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
        self.root.configure(bg=BG_COLOR)
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
        self.setup_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.setup_frame.pack(expand=True, fill='both')
        
        tk.Label(self.setup_frame, text="WORDLE 6+", font=("Helvetica", 42, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(120, 20))
        tk.Label(self.setup_frame, text="Đồ án môn DSA (Cấu trúc dữ liệu)", font=("Helvetica", 14), bg=BG_COLOR, fg=KEY_BG).pack(pady=(0, 40))
        
        tk.Label(self.setup_frame, text="Vui lòng chọn độ khó:", font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
        
        tk.Button(self.setup_frame, text="Dễ (Easy)", font=("Helvetica", 14), bg=CORRECT_COLOR, fg=TEXT_COLOR, 
                  activebackground="#43723e", activeforeground="white", command=lambda: self.start_game('easy')).pack(pady=5, ipadx=40, ipady=5)
                  
        tk.Button(self.setup_frame, text="Trung bình (Medium)", font=("Helvetica", 14), bg=PRESENT_COLOR, fg=TEXT_COLOR, 
                  activebackground="#968331", activeforeground="white", command=lambda: self.start_game('medium')).pack(pady=5, ipadx=10, ipady=5)
                  
        tk.Button(self.setup_frame, text="Khó (Hard)", font=("Helvetica", 14), bg=ABSENT_COLOR, fg=TEXT_COLOR, 
                  activebackground="#2b2b2d", activeforeground="white", command=lambda: self.start_game('hard')).pack(pady=5, ipadx=40, ipady=5)

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
        tk.Label(self.root, text="WORDLE", font=("Helvetica", 28, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(20, 10))
        
        # Grid chữ cái
        self.grid_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.grid_frame.pack(pady=10)
        
        self.labels = []
        for i in range(8):
            row_labels = []
            for j in range(6):
                # Tạo các ô label trống để chứa chữ cái
                lbl = tk.Label(self.grid_frame, text="", font=("Helvetica", 24, "bold"), bg=BG_COLOR, fg=TEXT_COLOR, 
                               width=3, height=1, relief="solid", borderwidth=1, highlightbackground=BORDER_COLOR)
                lbl.grid(row=i, column=j, padx=4, pady=4)
                row_labels.append(lbl)
            self.labels.append(row_labels)
            
        # Keyboard ảo dước đáy màn hình
        self.keyboard_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.keyboard_frame.pack(pady=30)
        
        self.keys = {}
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for r_idx, row in enumerate(rows):
            row_frame = tk.Frame(self.keyboard_frame, bg=BG_COLOR)
            row_frame.pack(pady=3)
            
            # Cột hàng thứ 3 có thêm phím ENTER
            if r_idx == 2:
                btn = tk.Button(row_frame, text="ENTER", font=("Helvetica", 10, "bold"), bg=KEY_BG, fg=TEXT_COLOR, 
                                command=self.submit_guess, width=6, borderwidth=0)
                btn.pack(side="left", padx=3, ipady=8)
                
            for char in row:
                btn = tk.Button(row_frame, text=char, font=("Helvetica", 11, "bold"), bg=KEY_BG, fg=TEXT_COLOR, 
                                width=3, borderwidth=0, command=lambda c=char: self.type_char(c))
                btn.pack(side="left", padx=2, ipady=8)
                self.keys[char] = btn
                
            # Cột hàng thứ 3 có thêm phím XÓA (Backspace)
            if r_idx == 2:
                btn = tk.Button(row_frame, text="⌫", font=("Helvetica", 12), bg=KEY_BG, fg=TEXT_COLOR, 
                                command=self.delete_char, width=4, borderwidth=0)
                btn.pack(side="left", padx=3, ipady=8)

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
                self.labels[self.current_row][i].config(text=self.current_guess[i], relief="solid", borderwidth=2)
            else:
                self.labels[self.current_row][i].config(text="", relief="solid", borderwidth=1)

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
        
        # Mở màu trên lướt Grid
        for i, (char, status) in enumerate(eval_result):
            color = BG_COLOR
            if status == Game.CORRECT:
                color = CORRECT_COLOR
            elif status == Game.PRESENT:
                color = PRESENT_COLOR
            else:
                color = ABSENT_COLOR
                
            self.labels[self.current_row][i].config(bg=color, fg=TEXT_COLOR, relief="flat")
            
        # Cập nhật màu lên bàn phím ảo
        for char, status in self.game.letter_status.items():
            if status == Game.CORRECT:
                self.keys[char].config(bg=CORRECT_COLOR)
            elif status == Game.PRESENT and self.keys[char]['bg'] != CORRECT_COLOR:
                self.keys[char].config(bg=PRESENT_COLOR)
            elif status == Game.ABSENT and self.keys[char]['bg'] not in [CORRECT_COLOR, PRESENT_COLOR]:
                self.keys[char].config(bg=ABSENT_COLOR)

        self.current_row += 1
        self.current_guess = ""
        
        if self.game.is_won:
            self.show_end_game_msg("✨ CHIẾN THẮNG ✨", f"Chúc mừng! Bạn đã đoán đúng từ \n'{self.game.answer}'\nsau {self.current_row} lượt.")
        elif self.game.is_over:
            self.show_end_game_msg("❌ THUA CUỘC ❌", f"Bạn đã hết lượt chơi.\nTừ hiển nhiên là: '{self.game.answer}'")

    def show_end_game_msg(self, title, message):
        """Hộp thoại cuối màn chơi"""
        response = messagebox.askyesno(title, f"{message}\n\nBạn có muốn chơi ván mới không?")
        if response:
            self.root.destroy()
            new_root = tk.Tk()
            app = WordleGUI(new_root)
            new_root.mainloop()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()
