import json
import math

positional_index_path = "data/positional_index.json"
news_path = "data/news.json"
output_path = "data/words_sorted_by_idf.json"

with open(positional_index_path, 'r', encoding='utf-8') as file:
    positional_index = json.load(file)

with open(news_path, 'r', encoding='utf-8') as file:
    news_data = json.load(file)

N = len(news_data)

word_info = []

for word, details in positional_index.items():
    document_count = len(details["documents"])
    if document_count == 0:
        continue
    idf = math.log(N / document_count)
    word_info.append({
        "word": word,
        "idf": idf,
        "document_count": document_count
    })

sorted_by_idf = sorted(word_info, key=lambda x: x["idf"], reverse=True)

with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(sorted_by_idf, file, ensure_ascii=False, indent=4)

print(f"کلمات بر اساس IDF مرتب شده و در فایل {output_path} ذخیره شدند.")
