import json
from collections import defaultdict

tf_idf_file = "data/tf_idf_vectors.json"
doc1_id = "74"
doc2_id = "75"

with open(tf_idf_file, 'r', encoding='utf-8') as file:
    tf_idf_vectors = json.load(file)
    
tf_idf_doc1 = tf_idf_vectors[doc1_id]
tf_idf_doc2 = tf_idf_vectors[doc2_id]
combined_vector = defaultdict(float)

for word, weight in tf_idf_doc1.items():
    combined_vector[word] += weight
for word, weight in tf_idf_doc2.items():
    combined_vector[word] += weight
    
combined_vector = dict(combined_vector)

print(f"بردار TF-IDF سند {doc1_id}:")
for word, weight in tf_idf_doc1.items():
    print(f"{word}: {weight:.4f}")
print(f"\nبردار TF-IDF سند {doc2_id}:")
for word, weight in tf_idf_doc2.items():
    print(f"{word}: {weight:.4f}")
print(f"\nبردار TF-IDF ترکیبی (سند {doc1_id} + سند {doc2_id}):")
for word, weight in sorted(combined_vector.items(), key=lambda x: x[1], reverse=True):
    print(f"{word}: {weight:.4f}")
