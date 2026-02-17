import math
import json
from collections import defaultdict
from hazm import Normalizer, word_tokenize, Stemmer

normalizer = Normalizer()
stemmer = Stemmer()

with open("data/positional_index.json", 'r', encoding='utf-8') as file:
    positional_index = json.load(file)

with open("data/tf_idf_vectors.json", 'r', encoding='utf-8') as file:
    tf_idf_vectors = json.load(file)

N = len(tf_idf_vectors)

def calculate_query_tfidf(query, positional_index, N):
    query_tokens = word_tokenize(normalizer.normalize(query))
    query_stems = [stemmer.stem(token) for token in query_tokens]

    query_tf = defaultdict(int)
    for term in query_stems:
        query_tf[term] += 1

    query_tfidf = {}
    for term, freq in query_tf.items():
        if term in positional_index:
            idf = math.log(N / len(positional_index[term]["documents"]))
            tf = 1 + math.log(freq)
            query_tfidf[term] = tf * idf
    return query_tfidf

def cosine_similarity(vec1, vec2):
    dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in vec1.keys())
    magnitude_vec1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    magnitude_vec2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0
    return dot_product / (magnitude_vec1 * magnitude_vec2)

query = input("پرسمان خود را وارد کنید: ")

query_tfidf = calculate_query_tfidf(query, positional_index, N)

similarities = {}
for doc_id, doc_vector in tf_idf_vectors.items():
    similarity = cosine_similarity(query_tfidf, doc_vector)
    similarities[doc_id] = similarity

sorted_docs = sorted(similarities.items(), key=lambda item: item[1], reverse=True)

print("اسناد مشابه با پرسمان:")
for doc_id, similarity in sorted_docs[:10]:
    print(f"سند {doc_id}: تشابه = {similarity:.4f}")
