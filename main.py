import sys
import os

from word_manager import WordManager
from game import Game
from ui import UI

def main():
    """
    Điểm bắt đầu của ứng dụng Wordle (cốt lõi vòng lặp chính của trò chơi).
    Chịu trách nhiệm khởi tạo manager, game logic và xử lý thông điệp gửi tới UI.
    """
    try:
        # Đường dẫn file danh sách từ
        base_dir = os.path.dirname(os.path.abspath(__file__))
        words_file = os.path.join(base_dir, 'words.txt')
        
        # Khởi tạo quản lý danh sách từ
        manager = WordManager(words_file)
    except FileNotFoundError as e:
        print(f"Lỗi khởi tạo danh sách từ: {e}")
        sys.exit(1)
        
    try:
        # Lấy từ ngẫu nhiên
        answer = manager.get_random_word()
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
