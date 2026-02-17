import os
import re
import json
from collections import Counter, defaultdict
from hazm import Normalizer, word_tokenize, Stemmer
import math

file_path = "data/news.json"
positional_index_path = "data/positional_index.json"
tf_idf_output_path = "data/tf_idf_vectors.json"

normalizer = Normalizer()
stemmer = Stemmer()
word_counter = Counter()

if os.path.exists(positional_index_path):
    with open(positional_index_path, 'r', encoding='utf-8') as file:
        positional_index = json.load(file)
    print("شاخص مکانی از فایل بارگذاری شد.")
else:
    print("شاخص مکانی وجود ندارد. در حال ساخت...")
    positional_index = defaultdict(lambda: {"total_count": 0, "documents": {}})

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    processed_documents = {}

    for doc_id, doc_content in data.items():
        text = doc_content.get('content', '')

        original_tokens = word_tokenize(text)
        normalized_text = normalizer.normalize(text)
        cleaned_text = re.sub(r"[^\w\s‌]", "", normalized_text)
        tokens = word_tokenize(cleaned_text)
        stems = [stemmer.stem(token) for token in tokens]
        processed_documents[doc_id] = stems
        word_counter.update(stems)

        for idx, token in enumerate(original_tokens):
            stemmed_token = stemmer.stem(token)
            if stemmed_token not in positional_index:
                positional_index[stemmed_token]["documents"][doc_id] = {"positions": [], "count": 0}

            positional_index[stemmed_token]["total_count"] += 1
            if doc_id not in positional_index[stemmed_token]["documents"]:
                positional_index[stemmed_token]["documents"][doc_id] = {"positions": [], "count": 0}
            positional_index[stemmed_token]["documents"][doc_id]["positions"].append(idx)
            positional_index[stemmed_token]["documents"][doc_id]["count"] += 1

    most_common_words = [word for word, _ in word_counter.most_common(50)]
    for word in most_common_words:
        if word in positional_index:
            del positional_index[word]

    with open(positional_index_path, 'w', encoding='utf-8') as output_file:
        json.dump(positional_index, output_file, ensure_ascii=False, indent=4)
    print(f"شاخص مکانی در فایل {positional_index_path} ذخیره شد.")

N = len(data)
tf_idf_vectors = defaultdict(dict)

for term, details in positional_index.items():
    for doc_id, doc_info in details["documents"].items():
        tf = 1 + math.log(doc_info["count"])
        idf = math.log(N / len(details["documents"]))
        tf_idf = tf * idf
        tf_idf_vectors[doc_id][term] = tf_idf

with open(tf_idf_output_path, 'w', encoding='utf-8') as output_file:
    json.dump(tf_idf_vectors, output_file, ensure_ascii=False, indent=4)

print(f"مدل فضای برداری در فایل {tf_idf_output_path} ذخیره شد.")
