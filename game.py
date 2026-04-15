class Game:
    """
    Lớp quản lý trạng thái trò chơi Wordle.
    Theo dõi đáp án, lượt chơi và đánh giá suy luận của người dùng.
    """
    
    # Các trạng thái của một chữ cái sau khi kiểm tra
    CORRECT = "CORRECT"        # Đúng chữ, đúng vị trí (green)
    PRESENT = "PRESENT"        # Đúng chữ, sai vị trí (yellow)
    ABSENT = "ABSENT"          # Sai hoàn toàn (gray)
    
    def __init__(self, answer: str, max_guesses: int = 8):
        """
        Khởi tạo game với từ mục tiêu và số lượt đoán tối đa.
        
        Args:
            answer (str): Từ cần đoán (đáp án).
            max_guesses (int): Số lượt đoán tối đa.
        """
        self.answer = answer.upper()
        self.max_guesses = max_guesses
        self.guesses = []  # Lưu trữ các lần đoán
        self.letter_status = {chr(i): None for i in range(65, 91)} # Trạng thái các chữ cái A-Z
        self.is_won = False
        self.is_over = False

    def get_remaining_guesses(self) -> int:
        """
        Lấy số lượt đoán còn lại.
        """
        return self.max_guesses - len(self.guesses)

    def evaluate_guess(self, guess: str) -> list[tuple[str, str]]:
        """
        Đánh giá một từ được đoán so với đáp án.
        Mọi ký tự đều được biểu thị trạng thái (Tồn tại, Đúng, Sai).
        
        Thuật toán Wordle:
        1. Đánh dấu tất cả các chữ cái "Đúng" (màu Xanh)
        2. Dựa trên số lượng vị trí còn lại ở đáp án, đánh dấu chữ là "Sắp đúng" (màu Vàng)
        3. Các từ không khớp còn lại là "Sai" (màu Xám)
        
        Args:
            guess (str): Từ mà người dùng đoán.
            
        Returns:
            list[tuple[str, str]]: Danh sách chứa Tuple gồm kí tự và trạng thái của nó.
        """
        guess = guess.upper()
            
        result = [[char, self.ABSENT] for char in guess]
        answer_chars = list(self.answer)
        
        # Bước 1: Kiểm tra đúng vị trí (CORRECT)
        for i in range(min(len(guess), len(self.answer))):
            if guess[i] == answer_chars[i]:
                result[i][1] = self.CORRECT
                answer_chars[i] = None  # Đánh dấu đã dùng
                
        # Bước 2: Kiểm tra đúng chữ sai vị trí (PRESENT) dư và sai vị trí hoàn toàn (ABSENT)
        for i in range(len(guess)):
            if result[i][1] == self.CORRECT:
                continue
                
            char = guess[i]
            if char in answer_chars:
                result[i][1] = self.PRESENT
                # Đánh dấu là đã dùng để không báo vàng 2 lần cho 1 chữ có 1 lần xuất hiện
                answer_chars[answer_chars.index(char)] = None
                
        return [(item[0], item[1]) for item in result]

    def make_guess(self, guess: str) -> list[tuple[str, str]]:
        """
        Thực hiện một lượt đoán và cập nhật trạng thái game.
        
        Args:
            guess (str): Từ đoán của người chơi.
            
        Returns:
            list[tuple[str, str]]: Kết quả đánh giá của từ.
        """
        if self.is_over:
            raise ValueError("Trò chơi đã kết thúc!")
            
        guess = guess.upper()
        evaluation = self.evaluate_guess(guess)
        self.guesses.append(evaluation)
        
        # Cập nhật trạng thái bàn phím chữ cái
        for char, status in evaluation:
            current_status = self.letter_status.get(char)
            if status == self.CORRECT:
                self.letter_status[char] = self.CORRECT
            elif status == self.PRESENT and current_status != self.CORRECT:
                self.letter_status[char] = self.PRESENT
            elif status == self.ABSENT and current_status not in (self.CORRECT, self.PRESENT):
                self.letter_status[char] = self.ABSENT
        
        # Kiểm tra chiến thắng hoặc thua
        if guess == self.answer:
            self.is_won = True
            self.is_over = True
        elif len(self.guesses) >= self.max_guesses:
            self.is_over = True
            
        return evaluation
