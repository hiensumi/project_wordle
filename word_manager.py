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
        """
        self.words = set()
        self.easy_words = set()
        self.medium_words = set()
        self.hard_words = set()
        self.vn_words = set()
        
        self.base_dir = base_dir
        self._load_words()

    def _read_file(self, filename: str, is_vn: bool = False) -> set:
        """Đọc và trả về danh sách từ từ một file cụ thể."""
        filepath = os.path.join(self.base_dir, filename)
        words_set = set()
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().upper()
                    if is_vn:
                        if 1 <= len(word) <= 7:
                            words_set.add(word)
                    else:
                        if len(word) == 6 and word.isalpha():
                            words_set.add(word)
        return words_set

    def _load_words(self):
        """Đọc tất cả các file từ điển."""
        self.words = self._read_file('words.txt')
        self.easy_words = self._read_file('words_easy.txt')
        self.medium_words = self._read_file('words_medium.txt')
        self.hard_words = self._read_file('words_hard.txt')
        self.vn_words = self._read_file('words_vn.txt', is_vn=True)
        
        if not self.easy_words: self.easy_words = self.words.copy()
        if not self.medium_words: self.medium_words = self.words.copy()
        if not self.hard_words: self.hard_words = self.words.copy()

    def is_valid(self, word: str, lang: str = 'en') -> bool:
        """Kiểm tra xem một từ có hợp lệ không."""
        if lang == 'vn':
            return word.upper() in self.vn_words
        return word.upper() in self.words

    def get_random_word(self, difficulty: str = 'medium', lang: str = 'en') -> str:
        """Lấy một từ ngẫu nhiên làm đáp án."""
        if lang == 'vn':
            if not self.vn_words:
                raise ValueError("Danh sách từ vựng VN trống.")
            return random.choice(list(self.vn_words))
            
        if difficulty == 'easy':
            target_list = self.easy_words
        elif difficulty == 'hard':
            target_list = self.hard_words
        else:
            target_list = self.medium_words
            
        if not target_list:
            raise ValueError(f"Danh sách từ tiếng Anh ({difficulty}) trống.")
        return random.choice(list(target_list))
