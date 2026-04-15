import sys
import os

from word_manager import WordManager
from game import Game
from ui import UI

def main():
    """
    Điểm bắt đầu của ứng dụng Wordle (Môi trường Console).
    
    Hàm này chịu trách nhiệm khởi tạo đối tượng WordManager để nạp từ điển,
    thu nhận lựa chọn độ khó từ người chơi thông qua giao diện UI, thiết lập 
    logic cốt lõi qua đối tượng Game và duy trì vòng lặp trò chơi chính.
    Vòng lặp sẽ tiếp tục cho đến khi trò chơi kết thúc (thắng hoặc hết lượt) 
    hoặc khi người dùng yêu cầu thoát bằng từ khóa 'QUIT' hay 'EXIT'.
    
    Raises:
        SystemExit: Thoát chương trình nếu không tìm thấy file từ điển, 
                    hoặc khi người dùng chủ động thoát trò chơi.
    """
    try:
        # Thư mục gốc dự án
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Khởi tạo quản lý danh sách từ với base directory
        manager = WordManager(base_dir)
    except FileNotFoundError as e:
        print(f"Lỗi khởi tạo danh sách từ: {e}")
        sys.exit(1)
        
    # Chọn độ khó game
    UI.print_difficulty_menu()
    difficulty = UI.get_difficulty_choice()
        
    try:
        # Lấy từ ngẫu nhiên theo độ khó
        answer = manager.get_random_word(difficulty)
    except ValueError as e:
        print(f"Lỗi lấy từ ngẫu nhiên: {e}")
        sys.exit(1)
        
    # Khởi tạo trò chơi (giới hạn 8 lượt đoán, độ dài 6)
    max_guesses = 8
    word_length = 6
    game = Game(answer, max_guesses=max_guesses)
    
    # Hiển thị UI đầu game
    UI.print_header(max_guesses, word_length)
    
    while not game.is_over:
        # In ra bàn phím tình trạng chữ cái
        UI.print_keyboard(game.letter_status)

        # Lấy số lượt còn lại & yêu cầu nhập
        remains = game.get_remaining_guesses()
        prompt = f"Lượt đoán {game.max_guesses - remains + 1}/{game.max_guesses} > "
        guess = UI.get_user_input(prompt).upper()
        
        # Thoát nếu người dùng muốn dừng
        if guess in ("QUIT", "EXIT"):
            print(f"\n{UI.BOLD}Bạn đã thoát khỏi trò chơi. Từ mục tiêu là: {answer}{UI.RESET}")
            sys.exit(0)
            
        # Kiểm tra độ dài
        if len(guess) != word_length:
            print(f"{UI.YELLOW}Lỗi: Bạn phải nhập từ có {word_length} chữ cái.{UI.RESET}\n")
            continue
            
        # Kiểm tra tính hợp lệ trong danh sách (is_valid)
        if not manager.is_valid(guess):
            print(f"{UI.YELLOW}Lỗi: Từ không có trong từ điển.{UI.RESET}\n")
            continue
            
        # Thực hiện việc đoán và nhận về kết quả
        try:
            evaluation = game.make_guess(guess)
        except ValueError as e:
            print(f"{UI.YELLOW}Lỗi thực hiện: {e}{UI.RESET}\n")
            break
            
        # Hiển thị kết quả bằng UI console (màu)
        UI.print_guess(evaluation)
        print()
        
    # Kết thúc game
    if game.is_won:
        print(f"\n{UI.GREEN}{UI.BOLD}CHÚC MỪNG! BẠN ĐÃ ĐOÁN ĐÚNG SAU {len(game.guesses)} LƯỢT CHƠI.{UI.RESET}")
    else:
        print(f"\n{UI.GRAY}{UI.BOLD}THUA RỒI! TỪ CHÍNH XÁC LÀ: {answer}{UI.RESET}")

if __name__ == "__main__":
    main()
