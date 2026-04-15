import sys
from typing import List, Tuple

class UI:
    """
    Hệ thống thiết lập cơ sở tương tác qua Text/Command-Line Interface.
    
    Lớp này chuyên dụng xuất phản hồi thông tin trò chơi thông qua Console 
    (Terminal), được tích hợp bảng ANSI Escape code nguyên sinh trên Python chuẩn.
    Thúc đẩy mã định dạng cho bảng phím, giao diện Menu, giúp phân biệt rõ 
    những trạng thái của trò chơi mà không làm rối loạn người dùng hay vi phạm 
    tính kết hợp logic. Hoạt động tách rời theo dạng Interface chuẩn.
    """
    
    # Mã màu ANSI
    GREEN = '\033[92m'        # Đúng vị trí
    YELLOW = '\033[93m'       # Đúng chữ, sai vị trí
    GRAY = '\033[90m'         # Sai hoàn toàn
    RESET = '\033[0m'         # Reset màu sắc về mặc định
    BOLD = '\033[1m'          # Chữ in đậm
    
    # Kí hiệu của Game.py (tránh reference vòng hay coupling)
    CORRECT = "CORRECT"
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"

    @staticmethod
    def print_colored_char(char: str, status: str) -> None:
        """
        Dùng bộ tô màu tiêu chuẩn thay đổi tính chất Console cho đối tượng ký tự 
        trên đầu ra hệ thống, tùy thuộc vào kết quả Game gửi lại.
        
        Sóng nhận là: Xanh lá (CORRECT), Vàng (PRESENT) hoặc Màu tàn (ABSENT).
        
        Args:
            char (str): Ký hiệu đơn đại diện (Chữ cái cái đơn lẻ).
            status (str): Thẻ enum báo cáo màu tương đối (UI.CORRECT, etc.).
        """
        color = UI.RESET
        if status == UI.CORRECT:
            color = UI.GREEN
        elif status == UI.PRESENT:
            color = UI.YELLOW
        elif status == UI.ABSENT:
            color = UI.GRAY
            
        # In trực tiếp bằng màu
        sys.stdout.write(f"{UI.BOLD}{color}[ {char} ]{UI.RESET} ")
        sys.stdout.flush()

    @staTriển khai chuỗi hàm in lặp nhằm ánh xạ danh sách `evaluation` thành văn bản GUI 
        hoàn thiện cho toàn bộ độ dài của một từ giải.
        
        Duyệt liên tục trên mảng ký tự cho tới chiều dài giới hạn nhằm nối kết lại các màu.
        
        Args:
            evaluation (list[tuple[str, str]]): Một ArrayList chứa bản tổng hợp các Tuples 
                đóng gói kí tự từ được đoán với Enum trạng thái thuộc hạ của game
        
        Args:
            evaluation (list[tuple[str, str]]): Một list các tuple (ký tự, trạng thái).
        """
        for char, status in evaluation:
            UI.print_colored_char(char, status)
        print() # Xuống dòng

    @staticmethod
    def print_keyboard(letter_status: dict) -> None:
        """
        Bố cục hóa và xuất cấu hình QWERTY của danh mục chữ cái đánh giá lên màn hình chuẩn, 
        giúp xác định chữ nào đã sử dụng trước đó (lọc).
        
        Mô phỏng sự phản chiếu trạng thái thông qua `letter_status`, đánh màu riêng biệt bằng 
        cơ chế ANSI escape string.
        
        Args:
            letter_status (dict): Biến lưu lưu trạng thái (Dict[str, str]), Key đại diện 
                                 cho Char. Value giữ giá trị tình trạng từ GAME core.
        """
        rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        print("\nBàn phím trạng thái:")
        for row in rows:
            print(" " * (10 - len(row)), end="") # Căn giữa đơn giản
            for char in row:
                status = letter_status.get(char)
                color = UI.RESET # Trắng/Mặc định nếu chưa dùng
                
                if status == UI.CORRECT:
                    color = UI.GREEN
                elif status == UI.PRESENT:
                    color = UI.YELLOW
                elif status == UI.ABSENT:
                    color = UI.GRAY
                    
                sys.stdout.write(f"{UI.BOLD}{color}[{char}]{UI.RESET} ")
            print() # Xuống dòng cho mỗi row của bàn phím
        print() # Dòng trống cuối
        
    @staticmethod
    def print_header(max_guesses: int, word_length: int) -> None:
        """
        Triển khai in dòng tiêu đề khai mạc, đính kèm thông số kĩ thuật quan trọng và 
        phần giới thiệu phương thức hoạt động để người chơi nắm bắt quy tắc.
        
        Nội dung gồm có độ dài văn bản bắt buộc, số lượng vòng lặp đoán, hệ sinh thái màu.
        
        Args:
            max_guesses (int): Giới hạn sinh mệnh của một vòng đời cho phép.
            word_length (int): Ràng buộc từ gốc ở độ khó hiện tại.
        """
        print("="*40)
        print(f"{UI.BOLD} WORDLE GAME - PROJECT DSA {UI.RESET}".center(40 + len(UI.BOLD) + len(UI.RESET)))
        print("="*40)
        print(f"Luật chơi:")
        print(f"- Đoán một từ tiếng Anh có {word_length} chữ cái.")
        print(f"- Bạn có {max_guesses} lượt đoán.")
        print(f"- Ý nghĩa màu sắc:")
        print(f"  {UI.GREEN}[X]{UI.RESET}: Chữ cái đúng và nằm đúng vị trí.")
        print(f"  {UI.YELLOW}[Y]{UI.RESET}: Chữ cái có trong từ nhưng sai vị trí.")
        Hiển thị ra bộ phân chia menu cho người chơi có khả năng ra quyết định độ 
        cứng của từ loại trước khi bước vào ván game Wordle thật sự. 
        Văn bản có ứng dụng mã hóa giao thức CLII.RESET}: Chữ cái không có mặt trong từ.")
        print(f"- Gõ 'quit' hoặc 'exit' để thoát.")
        print("="*40 + "\n")

    @staticmethod
    def print_difficulty_menu() -> None:
        """
        In menu bảng chọn độ khó.
        Mở một giao thức nhập tiêu chuẩn (IO Input Queue) tiếp nhận số integer 
        chọn cấp độ từ 1-3, kèm khả năng tự động xử lý rác ruy băng trống `.strip()`.
        
        Bao bọc trong vòng lặp liên hoàn While-True phòng trừ giá trị nhập không tồn tại.
        
        Returns:
            str: Tên khóa nội bộ cấu trúc của hệ thống (`'easy'`, `'medium'` hoặc `'hard'`)
        print(f"{UI.BOLD}Chọn độ khó cho từ đích:{UI.RESET}")
        print(f"1. {UI.GREEN}Dễ (Easy){UI.RESET} - 1000 từ vựng phổ biến nhất")
        print(f"2. {UI.YELLOW}Trung bình (Medium){UI.RESET} - 3000 từ vựng phổ thông")
        print(f"3. {UI.GRAY}Khó (Hard){UI.RESET} - Hơn 25.000 từ vựng hiếm và chuyên ngành")

    @staticmethod
    def get_difficulty_choice() -> str:
        """
        Lấy lựa chọn độ khó từ người dùng.
        """
        while True:
            choice = input(f"Nhập lựa chọn của bạn (1/2/3) > ").strip()
            if choice == '1':
                return 'easy'
            elif choice == '2':
                return 'medium'
        Tiếp nhận và làm sạch dữ liệu văn bản từ phím bấm console.
        
        Đây là giao diện trung gian chịu trách nhiệm đọc dữ liệu mà người chơi 
        tiến hành thông qua Input Prompt được tùy biến đa dạng.
        
        Args:
            prompt (str): Text chờ (Prefix String) báo hiệu lượt nhập từ.
            
        Returns:
            str: Khối chuỗi kí tự thuần đã bị dọn dẹp sạch khoảng trắng (space bar
        """
        Nhập dữ liệu với prompt.
        
        Args:
            prompt (str): Text sẽ hiển thị ra.
            
        Returns:
            str: chuỗi do người dùng nhập (đã strip).
        """
        return input(prompt).strip()
