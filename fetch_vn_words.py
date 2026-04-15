import urllib.request
import urllib.error
import ssl
import re

def download_and_process():
    urls = [
        "https://raw.githubusercontent.com/trungtv/pyvi/master/pyvi/models/words.txt"
    ]
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    valid_words = set()
    vn_chars = set("aáàảãạăắằẳẵặâấầẩẫậbcdđeéèẻẽẹêếềểễệghiíìỉĩịklmnoóòỏõọôốồổỗộơớờởỡợpqrstuúùủũụưứừửữựvxyýỳỷỹỵ" + 
                   "AÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬBCDĐEÉÈẺẼẸÊẾỀỂỄỆGHIÍÌỈĨỊKLMNOÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢPQRSTUÚÙỦŨỤƯỨỪỬỮỰVXYÝỲỶỸỴ ")

    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, context=ctx)
            content = response.read().decode('utf-8')
            for line in content.splitlines():
                word = line.strip().upper()
                # Split by space or underscore (some lists use underscore)
                parts = re.split(r'[\s_]+', word)
                if 1 <= len(parts) <= 2:
                    joined_word = " ".join(parts)
                    # Check if all characters are valid Vietnamese characters or spaces
                    if all(c in vn_chars for c in joined_word) and len(joined_word) > 0:
                        valid_words.add(joined_word)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    valid_words_list = sorted(list(valid_words))
    
    print(f"Total 1-2 syllable Vietnamese words found: {len(valid_words_list)}")
    
    if len(valid_words_list) >= 5000:
        with open("words_vn.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(valid_words_list))
        print("Words successfully written to words_vn.txt")
    else:
        print("Not enough words found. Minimum 5000 required.")
        exit(1)

if __name__ == '__main__':
    download_and_process()
