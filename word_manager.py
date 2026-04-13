import random
import os

class WordManager:
    """
    Quản lý danh sách các từ hợp lệ cho trò chơi Wordle.
    Đọc từ file text và cung cấp các hàm kiểm tra từ hợp lệ hoặc chọn từ ngẫu nhiên.
    """
    def __init__(self, base_dir: str):
        """
        Khởi tạo WordManager bằng cách đọc danh sách từ từ file và phân loại độ khó.
        
        Args:
            base_dir (str): Thư mục chứa các file từ điển.
        """
        self.words = set()  # Tất cả từ hợp lệ (để kiểm tra nhập vào)
        self.easy_words = set()
        self.medium_words = set()
        self.hard_words = set()
        
        self.base_dir = base_dir
        self._load_words()

    def _read_file(self, filename: str) -> set:
        """Đọc và trả về danh sách từ từ một file cụ thể."""
        filepath = os.path.join(self.base_dir, filename)
        words_set = set()
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().upper()
                    if len(word) == 6 and word.isalpha():
                        words_set.add(word)
        return words_set

    def _load_words(self):
        """
        Đọc tất cả các file từ điển và phân loại độ khó.
        """
        # Từ vựng hợp lệ để đoán (Tổng hợp của tất cả)
        self.words = self._read_file('words.txt')
        
        # Phân loại để chọn đáp án
        self.easy_words = self._read_file('words_easy.txt')
        self.medium_words = self._read_file('words_medium.txt')
        self.hard_words = self._read_file('words_hard.txt')
        
        # Nếu thiếu danh sách chia độ khó (VD: chưa chạy build file), dự phòng = toàn bộ words
        if not self.easy_words: self.easy_words = self.words.copy()
        if not self.medium_words: self.medium_words = self.words.copy()
        if not self.hard_words: self.hard_words = self.words.copy()

    def is_valid(self, word: str) -> bool:
        """
        Kiểm tra xem một từ có hợp lệ không (có nằm trong danh sách và độ dài là 6).
        
        Args:
            word (str): Từ cần kiểm tra.
            
        Returns:
            bool: True nếu hợp lệ, ngược lại False.
        """
        return word.upper() in self.words

    def get_random_word(self, difficulty: str = 'medium') -> str:
        """
        Lấy một từ ngẫu nhiên từ danh sách làm đáp án cho trò chơi theo cấp độ.
        
        Args:
            difficulty (str): 'easy', 'medium', 'hard'
        Returns:
            str: Một từ ngẫu nhiên có 6 chữ cái.
        """
        if difficulty == 'easy':
            target_list = self.easy_words
        elif difficulty == 'hard':
            target_list = self.hard_words
        else: # medium làm mặc định
            target_list = self.medium_words
            
        if not target_list:
            raise ValueError(f"Danh sách từ ({difficulty}) trống.")
        return random.choice(list(target_list))
