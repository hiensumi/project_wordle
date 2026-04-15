import sys
from typing import List, Tuple

class UI:
    """
    Lớp xử lý việc in và cấu hình giao diện.
    Sử dụng mã hệ thống (ANSI sequences) để thay đổi màu sắc văn bản trên thiết bị đầu cuối.
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
        In một ký tự với màu tương ứng dựa vào kết quả đoán.
        
        Args:
            char (str): Kí tự để in.
            status (str): Trạng thái (CORRECT, PRESENT, ABSENT).
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

    @staticmethod
    def print_guess(evaluation: List[Tuple[str, str]]) -> None:
        """
        In toàn bộ kết quả của 1 từ đã đoán.
        
        Args:
            evaluation (list[tuple[str, str]]): Một list các tuple (ký tự, trạng thái).
        """
        for char, status in evaluation:
            UI.print_colored_char(char, status)
        print() # Xuống dòng

    @staticmethod
    def print_keyboard(letter_status: dict) -> None:
        """
        In bàn phím ảo hiển thị trạng thái các chữ cái đã được dùng.
        
        Args:
            letter_status (dict): Từ điển ánh xạ kí tự -> trạng thái của nó.
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
        In tiêu đề và hướng dẫn mở đầu trò chơi.
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
        print(f"  {UI.GRAY}[Z]{UI.RESET}: Chữ cái không có mặt trong từ.")
        print(f"- Gõ 'quit' hoặc 'exit' để thoát.")
        print("="*40 + "\n")

    @staticmethod
    def print_difficulty_menu() -> None:
        """
        In menu bảng chọn độ khó.
        """
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
            elif choice == '3':
                return 'hard'
            else:
                print(f"{UI.YELLOW}Lựa chọn không hợp lệ, vui lòng nhập lại.{UI.RESET}")

    @staticmethod
    def get_user_input(prompt: str) -> str:
        """
        Nhập dữ liệu với prompt.
        
        Args:
            prompt (str): Text sẽ hiển thị ra.
            
        Returns:
            str: chuỗi do người dùng nhập (đã strip).
        """
        return input(prompt).strip()
