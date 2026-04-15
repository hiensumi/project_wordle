class Game:
    """
    Lớp quản lý logic tổng thể và trạng thái trò chơi Wordle liên tục.
    
    Lưu trữ đáp án (Answer) và theo dõi sát sao tất cả tiến trình lặp vòng lặp đoán 
    (Guesses) của người chơi hiện tại, tiến hành đánh giá chi tiết (Evaluation) mức độ
    chính xác của chữ theo phân vùng vị trí. Hoạt động trên môi trường thuần không 
    phụ thuộc vào View/UI.
    """
    
    # Các trạng thái của một chữ cái sau khi kiểm tra
    CORRECT = "CORRECT"        # Đúng chữ, đúng vị trí (green)
    PRESENT = "PRESENT"        # Đúng chữ, sai vị trí (yellow)
    ABSENT = "ABSENT"          # Sai hoàn toàn (gray)
    
    def __init__(self, answer: str, max_guesses: int = 8):
        """
        Đóng gói một ván chơi (phiên bản trò chơi mới) sử dụng từ mục tiêu định mức.
        
        Args:
            answer (str): Đáp án nguyên bản bắt buộc phải đoán.
            max_guesses (int): Giới hạn lượng lần phán đoán thất bại của user. Mặc định: 8.
        """
        self.answer = answer.upper()
        self.max_guesses = max_guesses
        self.guesses = []  # Lưu trữ các lần đoán
        self.letter_status = {chr(i): None for i in range(65, 91)} # Trạng thái các chữ cái A-Z
        self.is_won = False
        self.is_over = False

    def get_remaining_guesses(self) -> int:
        """
        Truy xuất số lượt đoán còn lại nhằm theo dõi quyền hạn của Client.
        
        Returns:
            int: Con số còn lại.
        """
        return self.max_guesses - len(self.guesses)
Công thức duyệt từng kí tự đoán so với từ gốc xác định kết quả Wordle Game:
        
        Quy luật phân quyền ưu tiên:
        1. (Pass 1): Kiểm tra ký tự nào có nội tại và độ trùng chuẩn xác như mong muốn => trạng thái CORRECT.
        2. (Pass 2): Với phần còn sót lại, đánh số đếm tìm kiếm cho từng kí tự dư/ lệch dòng ở Answer,
                     khi tìm thấy một phân tử, ta khoanh vùng là PRESENT, nếu không còn thì coi như ABSENT.
        
        Thuật toán này giúp giải quyết việc nhập lặp thừa ký tự (VD: "APPLE" đáp án là "PEARL").
        
        Args:
            guess (str): Từ vựng chuỗi con phán đoán trong lần submit hiện tại.
            
        Returns:
            list[tuple[str, str]]: Mảng chuỗi trạng thái kết hợp theo từng vị trí (Ký tự, Lớp Enum màu)
            
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
                
        Giao diện API thao tác thực tế dành cho người dùng nạp một chuỗi để tham gia đoán game.
        
        Phương thức không chỉ gọi tới máy học thuật toán `evaluate_guess` tính điểm mà 
        còn tự động duy trì ghi chép (`history log`), cập nhật từ điển các chữ 
        đã tiêu thụ (`letter_status`). Nếu người chơi cạn sạch giới hạn hoặc 
        hoàn thành việc giải đố thành tựu thì set giá trị boolean `is_won` và `is_over`.
        
        Args:
            guess (str): Chuỗi người dùng gõ vào và mong muốn tìm được nghiệm hợp lệ.
            
        Raises:
            ValueError: Exception sinh ra khi hệ thống nhận được request chơi lúc bàn 
            đã `is_over = True`.
            
        Returns:
            list[tuple[str, str]]: Dữ liệu mảng sau khi qua đánh giá logic, chuyển lại 
            cho luồng giao diện để hiển thị phản hồi từ trò chơi
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
