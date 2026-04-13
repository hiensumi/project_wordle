import urllib.request
import os

def create_difficulty_banks():
    print("Đang tải danh sách tần suất từ vựng...")
    # Tải danh sách 50,000 từ tiếng Anh phổ biến nhất
    url = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2016/en/en_50k.txt"
    
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        
        common_6_letter_words = []
        for line in data.split('\n'):
            parts = line.strip().split(' ')
            if len(parts) >= 1:
                word = parts[0].upper()
                if len(word) == 6 and word.isalpha():
                    common_6_letter_words.append(word)

        # Đọc danh sách từ hợp lệ hiện tại (30k từ)
        with open('words.txt', 'r', encoding='utf-8') as f:
            valid_words = set(line.strip().upper() for line in f)

        # Lọc những từ phổ biến mà có mặt trong từ điển hợp lệ của chúng ta
        valid_common = [w for w in common_6_letter_words if w in valid_words]

        # Phân loại
        easy_words = valid_common[:1000] # 1000 từ phổ biến nhất: Dễ
        medium_words = valid_common[1000:4000] # 3000 từ phổ biến tiếp theo: Trung bình
        
        easy_set = set(easy_words)
        medium_set = set(medium_words)
        
        # Hard: Các từ còn lại trong từ điển (rất hiếm)
        hard_words = [w for w in valid_words if w not in easy_set and w not in medium_set]
        
        # Lưu vào các file tương ứng
        with open('words_easy.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(easy_words))
            
        with open('words_medium.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(medium_words))
            
        with open('words_hard.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(hard_words))
            
        print(f"✅ Đã chia độ khó:")
        print(f"  - Dễ (Easy): {len(easy_words)} từ")
        print(f"  - Trung bình (Medium): {len(medium_words)} từ")
        print(f"  - Khó (Hard): {len(hard_words)} từ")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    create_difficulty_banks()
