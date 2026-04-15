import random
import os

class WordManager:
    """
    Quản lý danh sách các từ vựng hợp lệ làm dữ liệu cho trò chơi Wordle.
    
    Lớp này đảm nhận việc đọc toàn bộ bộ từ điển (dictionaries) từ hệ thống tập tin 
    địa phương thành các cấu trúc Set trong Python để gia tăng ưu thế phân tích Big-O (O(1)) 
    khi kiểm tra hợp chuẩn (Validity). Cũng cung cấp khả năng điều phối độ phức tạp ngẫu nhiên 
    khi bắt đầu lượt mới.
    """
    def __init__(self, base_dir: str):
        """
        Khởi tạo thực thể WordManager, tự động định tuyến và phân loại danh sách.
        
        Args:
            base_dir (str): Thư mục gốc chứa các tệp văn bản từ vựng tĩnh 
                            (words.txt, words_easy.txt, v.v.).
        """
        self.words = set()
        self.easy_words = set()
        self.medium_words = set()
        self.hard_words = set()
        self.vn_words = set()
        
        self.base_dir = base_dir
        self._load_words()

    def _read_file(self, filename: str, is_vn: bool = False) -> set:
        """
        Đọc và phân tách danh sách từ khóa hợp lệ từ một tệp tin xác định.
        
        Dữ liệu được làm sạch bằng `.strip()`, đưa về chế độ In Hoàn toàn (`upper()`)
        nhằm tránh vi phạm ngữ nghĩa. Quá trình kiểm định cũng được triển khai 
        nhằm đảm bảo độ dài thiết lập (6 chữ cái đối với tiếng Anh, từ 1 tới 7 với tiếng Việt).
        
        Args:
            filename (str): Tên file muốn nạp (vd: 'words_easy.txt').
            is_vn (bool): Cờ quy định nếu là bộ từ vựng tiếng Việt. Mặc định là False.
            
        Returns:
            set: Tập hợp (hash-set) bao gồm tất cả các từ vựng thỏa mãn điều kiện tệp.
        """
        filepath = os.path.join(self.base_dir, filename)
        words_set = set()
        if 
        Phương thức hỗ trợ (helper logic) đọc đồng loạt đa nguồn tệp từ điển.
        
        Liên tục gọi _read_file để lôi kéo dữ liệu lên RAM phân theo 
        tiếng Anh (3 mức khó khăn) và tiếng Việt (1 chế độ tổng hợp).
        Giả phòng rủi ro: Nếu độ khó nhỏ hơn không tìm thấy sẽ chèn bộ master words.txt.
        
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
        
        Tra cứu O(1) chữ cái dự đoán (guess) với bộ nhớ trong từ điển chính.
        
        Args:
            word (str): Từ cần chuẩn hóa và kiểm tra.
            lang (str): Nhãn hiệu ngôn ngữ của môi trường, 'vn' đổi sang tiếng Việt.
           
        Trích xuất thông minh một kết cấu đáp án (chọn ngẫu nhiên) cho một lượt đầu mới.
        
        Sử dụng cơ chế random.choice qua một tập ánh xạ từ danh sách theo khó khăn chỉ định.
        
        Args:
            difficulty (str): Phân lớp lấy dữ liệu ('easy', 'medium', 'hard'). Mặc định 'medium'.
            lang (str): Dòng ngôn ngữ ('en' hoặc 'vn'). Mặc định 'en'.
            
        Raises:
            ValueError: Từ điển trống (có thể do lỗi đọc file nội tại rỗng).
            
        Returns:
            str: Đáp án dưới định dạng chuẩn hoa in hoa cho một bản Game mới nhất.
        
        Returns:
            bool: True nếu là một từ hợp ngữ pháp từ điển hiện hành, False nếu ngược lại.
        
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
