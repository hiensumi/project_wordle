import random
import os

class WordManager:
    """
    Quản lý danh sách các từ hợp lệ cho trò chơi Wordle.
    Đọc từ file text và cung cấp các hàm kiểm tra từ hợp lệ hoặc chọn từ ngẫu nhiên.
    """
    def __init__(self, filepath: str = 'words.txt'):
        """
        Khởi tạo WordManager bằng cách đọc danh sách từ từ file.
        
        Args:
            filepath (str): Đường dẫn đến file chứa danh sách từ. Mặc định là 'words.txt'.
        """
        self.words = set()
        self.filepath = filepath
        self._load_words()

    def _load_words(self):
        """
        Đọc và lưu trữ các từ hợp lệ có đúng 6 chữ cái từ file.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Không tìm thấy file {self.filepath}")
            
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().upper()
                if len(word) == 6 and word.isalpha():
                    self.words.add(word)

    def is_valid(self, word: str) -> bool:
        """
        Kiểm tra xem một từ có hợp lệ không (có nằm trong danh sách và độ dài là 6).
        
        Args:
            word (str): Từ cần kiểm tra.
            
        Returns:
            bool: True nếu hợp lệ, ngược lại False.
        """
        return word.upper() in self.words

    def get_random_word(self) -> str:
        """
        Lấy một từ ngẫu nhiên từ danh sách làm đáp án cho trò chơi.
        
        Returns:
            str: Một từ ngẫu nhiên có 6 chữ cái.
        """
        if not self.words:
            raise ValueError("Danh sách từ trống.")
        return random.choice(list(self.words))
