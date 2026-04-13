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
    def get_user_input(prompt: str) -> str:
        """
        Nhập dữ liệu với prompt.
        
        Args:
            prompt (str): Text sẽ hiển thị ra.
            
        Returns:
            str: chuỗi do người dùng nhập (đã strip).
        """
        return input(prompt).strip()
