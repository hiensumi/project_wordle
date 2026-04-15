import customtkinter as ctk
from tkinter import messagebox
import os
import bogo
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
    """
    Lớp quản lý Giao diện Người dùng Đồ họa (GUI) cho trò chơi Wordle.
    
    Lớp này sử dụng thư viện customtkinter để vẽ và cập nhật giao diện, 
    nhận thông tin đầu vào từ người chơi (thông qua bàn phím thực hoặc phím ảo),
    và tương tác với lõi logic Game. Ngoài ra, lớp đóng vai trò cầu nối
    giữa kiểm tra từ điển và quản lý trạng thái trò chơi (WordManager).
    """
    def __init__(self, root):
        """
        Khởi tạo giao diện WordleGUI.
        
        Args:
            root (customtkinter.CTk): Cửa sổ gốc của ứng dụng giao diện.
        """
        self.root = root
        self.root.title("Wordle DSA Visual")
        self.root.geometry("550x800")
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
        """
        Khởi tạo và hiển thị màn hình chọn độ khó trước khi trò chơi bắt đầu.
        
        Phương thức này vẽ khung chứa (Frame) với tiêu đề trò chơi và các nút 
        nhấn tương ứng với ba độ khó: Dễ, Trung bình, Khó cho tiếng Anh, và 
        độ khó tương đương cho tiếng Việt. Giao diện này sẽ bị hủy bỏ (destroy) 
        khi người dùng thiết lập xong lựa chọn.
        """
        self.setup_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.setup_frame.pack(expand=True, fill='both')
        
        ctk.CTkLabel(self.setup_frame, text="WORDLE 6+", font=("Helvetica", 42, "bold"), text_color=TEXT_COLOR).pack(pady=(120, 20))
        ctk.CTkLabel(self.setup_frame, text="Đồ án môn DSA (Cấu trúc dữ liệu)", font=("Helvetica", 14), text_color=KEY_BG).pack(pady=(0, 40))
        
        ctk.CTkLabel(self.setup_frame, text="Vui lòng chọn chế độ:", font=("Helvetica", 16, "bold"), text_color=TEXT_COLOR).pack(pady=10)
        
        ctk.CTkButton(self.setup_frame, text="Dễ (Easy)", font=("Helvetica", 14, "bold"), fg_color=CORRECT_COLOR, hover_color="#43723e", 
                      text_color=TEXT_COLOR, command=lambda: self.start_game('easy', lang='en'), height=45, width=200).pack(pady=10)
                  
        ctk.CTkButton(self.setup_frame, text="Trung bình (Medium)", font=("Helvetica", 14, "bold"), fg_color=PRESENT_COLOR, hover_color="#968331", 
                      text_color=TEXT_COLOR, command=lambda: self.start_game('medium', lang='en'), height=45, width=200).pack(pady=10)
                  
        ctk
        Khởi tạo logic trò chơi và thiết lập bàn cờ (board) dựa trên ngôn ngữ & mức khó.
        
        Xóa màn hình chọn độ khó hiện tại, yêu cầu WordManager chọn một từ ngẫu 
        nhiên dựa theo độ khó, sau đó khởi tạo đối tượng Game tương ứng với từ này.
        Khung lưới giao diện và bàn phím tương tác sau đó được xây dựng thông qua
        phương thức `build_ui()`.
        
        Args:
            difficulty (str): Từ khóa chỉ định độ khó ('easy', 'medium', 'hard').
            lang (str, optional): Ký hiệu ngôn ngữ ('en' hoặc 'vn'). Mặc định là 'en'.
        d)", font=("Helvetica", 14, "bold"), fg_color=ABSENT_COLOR, hover_color="#2b2b2d", 
                      text_color=TEXT_COLOR, command=lambda: self.start_game('hard', lang='en'), height=45, width=200).pack(pady=10)
                      
        ctk.CTkButton(self.setup_frame, text="Tiếng Việt (1 Tiếng)", font=("Helvetica", 14, "bold"), fg_color="#4B0082", hover_color="#3A006F", 
                      text_color=TEXT_COLOR, command=lambda: self.start_game('medium', lang='vn'), height=45, width=200).pack(pady=10)

    def start_game(self, difficulty, lang='en'):
        """Khởi tạo Board cho Game sau khi chọn độ khó"""
        self.setup_frame.destroy()
        
        self.lang = lang
        self.answer = self.manager.get_random_word(difficulty, lang)
        self.game = Game(self.answer, max_guesses=8)
        
        Xây dựng khung lưới bảng chơi và bố trí bàn phím ảo (virtual keyboard).
        
        Tạo động lưới chứa các nhãn chữ cái theo chiều dài cột (dựa trên giới hạn 
        chữ cái của màn chơi) và tổng số hàng (đại diện cho số lượt đoán định mức 8).
        Bàn phím ảo được xây dựng với phím theo bố cục QWERTY hoặc tiếng Việt.
        
        self.current_guess = ""
        self.hidden_buffer = ""
        self.columns = 7 if self.lang == 'vn' else 6
        self.current_row = 0
        self.is_animating = False
        
        self.build_ui()
        self.root.bind("<Key>", self.handle_keypress)
        
    def build_ui(self):
        """Xây dựng khung lưới bảng chơi và bàn phím"""
        ctk.CTkLabel(self.root, text="WORDLE", font=("Helvetica", 28, "bold"), text_color=TEXT_COLOR).pack(pady=(20, 5))
        if self.lang == 'vn':
            ctk.CTkLabel(self.root, text="Đoán từ gồm 1 tiếng, độ dài ẩn (max 7 chữ)", font=("Helvetica", 14), text_color=TEXT_COLOR).pack(pady=(0, 10))
        else:
            ctk.CTkLabel(self.root, text="", font=("Helvetica", 14)).pack(pady=(0, 10))
            
        # Grid chữ cái
        self.grid_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.grid_frame.pack(pady=5)
        
        self.labels = []
        for i in range(8):
            row_labels = []
            for j in range(self.columns):
                # Bọc trong Frame con để vẽ viền siêu mảnh, chống giật font CTkLabel
                container = ctk.CTkFrame(self.grid_frame, fg_color=BG_COLOR, width=54, height=54, 
                                         border_width=2, border_color="#3a3a3c", corner_radius=4)
                container.grid(row=i, column=j, padx=4, pady=4)
                container.grid_propagate(False)
                
                # Khung chữ cải tiến: Có viền (border) nét 2px chuẩn gốc
                lbl = ctk.CTkLabel(container, text="", font=("Helvetica", 24, "bold"), text_color=TEXT_COLOR, 
                                   width=50, height=50, fg_color=BG_COLOR, corner_radius=2)
                lbl.place(relx=0.5, rely=0.5, anchor="center")
                
                row_labels.append({"lbl": lbl, "container": container})
            self.labels.append(row_labels)
            
        # Keyboard ảo dưới đáy màn hình
        self.keyboard_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.keyboard_frame.pack(pady=20)
        
        self.keys = {}
        if self.lang == 'vn':
            # Bàn phím chuẩn 29 chữ cái + 5 dấu
            rows = [
                [('Ă','Ă'), ('Â','Â'), ('Đ','Đ'), ('Ê','Ê'), ('Ô','Ô'), ('Ơ','Ơ'), ('Ư','Ư')],
                [('Q','Q'), ('E','E'), ('R','R'), ('T','T'), ('Y','Y'), ('U','U'), ('I','I'), ('O','O'), ('P','P')],
                [('A','A'), ('S','S'), ('D','D'), ('G','G'), ('H','H'), ('K','K'), ('L','L')],
                [('X','X'), ('C','C'), ('V','V'), ('B','B'), ('N','N'), ('M','M')],
                [('´ (Sắc)','S'), ('` (Huyền)','F'), ('? (Hỏi)','R'), ('~ (Ngã)','X'), ('. (Nặng)','J')]
            ]
            last_row_idx = 4
        else:
            rows = [
                [(c,c) for c in "QWERTYUIOP"],
                [(c,c) for c in "ASDFGHJKL"],
                [(c,c) for c in "ZXCVBNM"]
            ]
            last_row_idx = 2
            
        for r_idx, row in enumerate(rows):
            row_frame = ctk.CTkFrame(self.keyboard_frame, fg_color=BG_COLOR)
            row_frame.pack(pady=3)
            
            if r_idx == last_row_idx:
           
        Xử lý sự kiện nhấn phím trên bàn phím vật lý từ hệ thống.
        
        Args:
            event (tkinter.Event): Đối tượng biểu diễn sự kiện bàn phím.
        text="ENTER", font=("Helvetica", 12, "bold"), fg_color=KEY_BG, text_color=TEXT_COLOR, 
                                    command=self.submit_guess, width=65, height=45, hover_color="#6c6e6f")
                btn.pack(side="left", padx=3)
                
            for display_char, internal_char in row:
                btn = ctk.CTkButton(row_frame, text=display_char, font=("Helvetica", 14, "bold"), fg_color=KEY_BG, text_color=TEXT_COLOR, 
                                    width=40 if len(display_char) == 1 else 75, 
                                    height=45, command=lambda c=internal_char: self.type_char(c), hover_color="#6c6e6f")
                btn.pack(side="left", padx=2)
                self.keys[internal_char] = btn
                
            if r_idx == last_row_idx:
                btn = ctk.CTkButton(row_frame, text="⌫", font=("Helvetica", 16), fg_color=KEY_BG, text_color=TEXT_COLOR, 
                                    command=self.delete_char, width=50, height=45, hover_color="#6c6e6f")
                btn.pack(side="left", padx=3)

    def handle_keypress(self, event):
        """Xử lý sự kiện khi gõ bàn phím vật lý"""
        if self.game.is_over or self.is_animating: return
        
        char = event.char
        if char.isalpha() and len(char) == 1:
            self.type_char(char.upper())
        elif event.keysym == "BackSpace":
            self.delete_char()
        elif event.keysym == "Return":
            self.submit_guess()

    def type_char(self, char):
        """
        Xử lý khi người dùng nhập một chữ cái mới từ bàn phím (ảo hoặc vật lý).
        Hỗ trợ cập nhật lưới UI và xử lý gõ chuẩn tiếng Việt thông qua thư viện Bogo.
        
        Args:
            char (str): Kí tự vừa được người dùng nhập (chuỗi có độ dài 1).
        """
        if self.game.is_over or self.is_animating: return
        if self.lang == 'vn':
            new_buffer = self.hidden_buffer + char.lower()
            processed = bogo.process_sequence(new_buffer).upper()
            if len(processed) <= self.columns:
                self.hidden_buffer = new_buffer
                self.current_guess = processed
                self.update_current_row()
        else:
            if len(self.current_guess) < self.columns:
                self.current_guess += char
                self.update_current_row()

    def delete_char(self):
        """
        Xóa chữ cái cuối cùng trong từ đang được đoán hiện tại.
        Hỗ trợ quản lý lại bộ đệm gõ Telex nếu ngôn ngữ đang chơi là tiếng Việt.
        """
        if self.game.is_over or self.is_animating: return
        if self.lang == 'vn':
            if len(self.hidden_buffer) > 0:
                self.hidden_buffer = self.hidden_buffer[:-1]
                self.current_guess = bogo.process_sequence(self.hidden_buffer).upper()
                self.update_current_row()
        else:
            if len(self.current_guess) > 0:
        """
        Đồng bộ giao diện hàng lưới người dùng đang đoán với bộ đệm `current_guess`.
        
        Trường hợp người chơi bổ sung ký tự: Nền nút được cấu hình nổi bật (pop-up).
        Ngược lại, nếu xóa thì ô ký tự trở về màu tối nguyên thủy.
        """
                self.current_guess = self.current_guess[:-1]
                self.update_current_row()

    def update_current_row(self):
        for i in range(self.columns):
            if i < len(self.current_guess):
                # Khi đang gõ phím: Bo viền sáng (#565758), nháy khung pop nhẹ
                self.labels[self.current_row][i]["lbl"].configure(text=self.current_guess[i])
                self.labels[self.current_row][i]["container"].configure(border_color="#565758", border_width=3)
                
                # Popup nhẹ (Lùi border về width 2 nhanh chóng sau 100ms)
                self.root.after(100, lambda c=self.labels[self.current_row][i]["container"]: c.configure(border_width=2))
           
        Hiển thị một thông báo nổi (Toast message) trên UI đồ họa.
        
        Thông báo được dùng để báo lỗi ngữ pháp, không đủ độ dài, từ không tồn tại, v.v.
        Một nhãn (label) tạm thời sẽ xuất hiện trên màn hình và tự động biến mất 
        sau một thời gian định sẵn (1.5 giây).
        
        Args:
            message (str): Nội dung thông báo hiển thị cho người dùng.
        """
        Chấp nhận lượt đoán từ người chơi và truyền cho Game API để xử lý.
        
        Bao bọc các bước: Ngăn chặn nộp từ sai độ dài, kiểm tra sự tồn tại trong 
        từ điển với sự trợ giúp của WordManager, tính toán màu sắc trả về.
        Tiến hành hiệu ứng giao diện nếu tất cả đều được thông qua.
        """
        
                # Xóa kí tự: Về trạng thái tối nguyên thủy
                self.labels[self.current_row][i]["lbl"].configure(text="")
                self.labels[self.current_row][i]["container"].configure(border_color="#3a3a3c", border_width=2)

    def show_toast(self, message):
        """Hiển thị thông báo Toast siêu mượt không làm rung màn hình"""
        toast = ctk.CTkLabel(self.root, text=message, fg_color=TEXT_COLOR, text_color=BG_COLOR, 
                             corner_radius=4, font=("Helvetica", 14, "bold"), width=0)
        # padding inner của text
        toast.configure(padx=20, pady=10)
        toast.place(relx=0.5, rely=0.05, anchor="n")
        self.root.after(1500, toast.destroy)

    def submit_guess(self):
        if self.game.is_over or self.is_animating: return
        
        if self.lang == 'en' and len(self.current_guess) != self.columns:
            self.show_toast(f"Từ bạn nhập phải có đủ {self.columns} chữ cái!")
            return
        elif self.lang == 'vn' and len(self.current_guess) == 0:
            return
            
        if not self.manager.is_valid(self.current_guess, lang=self.lang):
            self.show_toast("Không có trong từ điển!" if self.lang == 'vn' else "Từ này không có trong từ điển tiếng Anh!")
            return
            
        # Nạp từ vào logic game
        eval_result = self.game.make_guess(self.current_guess)
        
        # Bắt đầu chuỗi animation lật ô màu
        self.is_animating = True
        self.animate_reveal(0, eval_result)

    def get_base_char(self, char):
        """
        Chuẩn hóa chữ cái có dấu để có thể tô màu tương ứng trên bàn phím ảo.
        Tiếng Việt sử dụng bảng dấu phong phú, cần ánh xạ lại kí tự nguyên mẫu (base)
        để màu sắc phản chiếu đúng theo luật chơi.
        
        Args:
            char (str): Ký tự đơn được truyền từ máy tính.
            
        Returns:
            str: Chữ cái in hoa nguyên bản không dấu.
        """
        if self.lang == 'en': return char
        mapping = {
            'Á': 'A', 'À': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
            'Ấ': 'Â', 'Ầ': 'Â', 'Ẩ': 'Â', 'Ẫ': 'Â', 'Ậ': 'Â',
            'Ắ': 'Ă', 'Ằ': 'Ă', 'Ẳ': 'Ă', 'Ẵ': 'Ă', 'Ặ': 'Ă',
            'É': 'E', 'È': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
            'Ế': 'Ê', 'Ề': 'Ê', 'Ể': 'Ê', 'Ễ': 'Ê', 'Ệ': 'Ê',
            'Í': 'I', 'Ì': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
            'Ó': 'O', 'Ò': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
            'Ố': 'Ô', 'Ồ': 'Ô', 'Ổ': 'Ô', 'Ỗ': 'Ô', 'Ộ': 'Ô',
            'Ớ': 'Ơ', 'Ờ': 'Ơ', 'Ở': 'Ơ', 'Ỡ': 'Ơ', 'Ợ': 'Ơ',
            'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
            'Ứ': 'Ư', 'Ừ': 'Ư', 'Ử': 'Ư', 'Ữ': 'Ư', 'Ự': 'Ư',
            'Ý': 'Y', 'Ỳ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
        }
        return mapping.get(char, char)

    def animate_reveal(self, col, eval_result):
        """
        Hệ thống giả lập hoạt ảnh lật từng ô vuông chữ cái để thông báo trạng thái.
        
        Thực hiện gọi đệ quy tuyến tính bằng UI After Timer để tạo cảm giác lật mở (flip).
        Mỗi lần cập nhật trạng thái màu cho ô ở cột tương ứng (đúng, sai, xám), 
        giao diện bàn phím trực tuyến cũng được áp dụng màu nền song song.
        
        Args:
            col (int): Chỉ mục cột chữ cái trên hàng hiện tại đang lật.
            eval_result (List[Tuple[str, str]]): List tuple chứa đánh giá 
                từ Game: (màu, trạng thái) của các vị trí từ vựng người dùng đưa vào.
        """
        if col < len(eval_result):
            char, status = eval_result[col]
            
            color = BG_COLOR
            if status == Game.CORRECT:
                color = CORRECT_COLOR
            elif status == Game.PRESENT:
                color = PRESENT_COLOR
            else:
                color = ABSENT_COLOR
                
            # Đổi màu nền, đồng thời tắt viền để ô đầy đặn (border match background)
            self.labels[self.current_row][col]["container"].configure(fg_color=color, border_width=0)
            self.labels[self.current_row][col]["lbl"].configure(fg_color=color)
            
            # Cập nhật màu lên bàn phím ảo tương ứng ngay lập tức
            base_char = self.get_base_char(char)
            if base_char in self.keys:
                current_bg = self.keys[base_char].cget("fg_color")
                if status == Game.CORRECT:
                    self.keys[base_char].configure(fg_color=CORRECT_COLOR, hover_color=CORRECT_COLOR)
                elif status == Game.PRESENT and current_bg != CORRECT_COLOR:
                    self.keys[base_char].configure(fg_color=PRESENT_COLOR, hover_color=PRESENT_COLOR)
                elif status == Game.ABSENT and current_bg not in [CORRECT_COLOR, PRESENT_COLOR]:
                    self.keys[base_char].configure(fg_color=ABSENT_COLOR, hover_color=ABSENT_COLOR)
            
            # Gọi đệ quy hàm để lật ô kế tiếp sau 150ms (Nhanh, dứt khoát hơn 250ms)
            self.root.after(150, self.animate_reveal, col + 1, eval_result)
        else:
            # Khi đã lật đủ chiều dài của từ:
            self.is_animating = False
            self.current_row += 1
           
        Hiển thị hộp thoại kết thúc lượt chơi Game Over.
        Hỏi người chơi xem có muốn chơi tiếp ván thứ hai với độ khó tương tự không.
        
        Args:
            title (str): Tiêu đề hộp thoại thông báo.
            message (str): Thông điệp truyền tải sau trận, thường bao gồm
                đáp án hoặc/và số lượt để thắng cuộc.
        "
            if self.lang == 'vn':
                self.hidden_buffer = ""
            
            # Đợi một nhịp 300ms rồi mới kết thúc để người chơi kịp nhìn màu
            if self.game.is_won:
                self.root.after(300, lambda: self.show_end_game_msg("✨ TỪ CHÍNH XÁC ✨", f"Chúc mừng! Bạn đã đoán đúng từ \n'{self.game.answer}'\nsau {self.current_row} lượt."))
            elif self.game.is_over:
                self.root.after(300, lambda: self.show_end_game_msg("❌ HẾT LƯỢT ❌", f"Bạn đã hết lượt đoán.\nTừ chính xác là: '{self.game.answer}'"))

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
