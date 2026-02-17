import json
import math
import re
import sys
from collections import Counter
from hazm import Normalizer, word_tokenize, Stemmer

normalizer = Normalizer()
stemmer = Stemmer()

def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)
    data_list = []
    for k, v in data_dict.items():
        data_list.append({
            'id': int(k),
            'content': v.get('content', '')
        })
    return data_list

def preprocess_text_basic(text):
    text = normalizer.normalize(text)
    text = re.sub(r"[^\w\s‌]", "", text)
    tokens = word_tokenize(text)
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens

def remove_punc_and_digits(tokens):
    cleaned = []
    for t in tokens:
        t = re.sub(r'[^\u0600-\u06FF\s]+', '', t)
        t = t.strip()
        if t:
            cleaned.append(t)
    return cleaned

def build_inverted_index_positional(docs_pos):
    idx = {}
    for d in docs_pos:
        did = d['id']
        for pos, token in enumerate(d['tokens']):
            if token not in idx:
                idx[token] = {}
            if did not in idx[token]:
                idx[token][did] = []
            idx[token][did].append(pos)
    return idx

def build_global_frequency_dict(docs):
    freq_dict = Counter()
    for d in docs:
        for t in d['tokens']:
            freq_dict[t] += 1
    return freq_dict

def remove_top_frequent_words(docs, freq_dict, n=50):
    mc = freq_dict.most_common(n)
    for w, c in mc:
        print(w, c)
    s = set([w for w, _ in mc])
    for d in docs:
        d['tokens'] = [x for x in d['tokens'] if x not in s]
    return docs

def apply_stemming_lemmatizing(docs):
    for d in docs:
        new_tokens = []
        for t in d['tokens']:
            s = stemmer.stem(t)
            new_tokens.append(s)
        d['tokens'] = new_tokens
    return docs

def build_tfidf_index(docs, n):
    inv = {}
    for d in docs:
        did = d['id']
        for t in d['tokens']:
            if t not in inv:
                inv[t] = {}
            if did not in inv[t]:
                inv[t][did] = 0
            inv[t][did] += 1
    tfidf_index = {}
    for token, posting in inv.items():
        c = len(posting)
        idf = math.log10(n / c) if c > 0 else 0
        for did, freq in posting.items():
            tf = 1 + math.log10(freq) if freq > 0 else 0
            val = tf * idf
            if token not in tfidf_index:
                tfidf_index[token] = {}
            tfidf_index[token][did] = val
    return tfidf_index

def build_query_vector(query, tfidf_index, n):
    from collections import Counter
    freq = Counter(preprocess_text_basic(query))
    qv = {}
    for token, fq in freq.items():
        tf = 1 + math.log10(fq) if fq > 0 else 0
        if token in tfidf_index:
            c = len(tfidf_index[token])
            idf = math.log10(n / c) if c > 0 else 0
        else:
            idf = 0
        qv[token] = tf * idf
    return qv

def cosine_similarity(qv, doc_id, tfidf_index):
    num = 0
    nq = 0
    nd = 0
    for token, w_q in qv.items():
        w_d = 0
        if token in tfidf_index and doc_id in tfidf_index[token]:
            w_d = tfidf_index[token][doc_id]
        num += w_q * w_d
        nq += (w_q ** 2)
        nd += (w_d ** 2)
    if nq == 0 or nd == 0:
        return 0
    return num / (math.sqrt(nq) * math.sqrt(nd))

def rank_documents(query, docs, tfidf_index):
    qv = build_query_vector(query, tfidf_index, len(docs))
    scores = []
    for d in docs:
        did = d['id']
        sim = cosine_similarity(qv, did, tfidf_index)
        scores.append((did, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def get_inverted_index_memory_size(inverted_index):
    size = 0
    for token, posting_dict in inverted_index.items():
        size += sys.getsizeof(token)
        size += sys.getsizeof(posting_dict)
        for doc_id, positions in posting_dict.items():
            size += sys.getsizeof(doc_id)
            size += sys.getsizeof(positions)
            for pos in positions:
                size += sys.getsizeof(pos)
    return size

if __name__ == "__main__":
    path = "data/news.json"
    raw_data = load_data(path)
    
    docs_pos = []
    for d in raw_data:
        toks = preprocess_text_basic(d['content'])
        toks = remove_punc_and_digits(toks)
        docs_pos.append({
            'id': d['id'],
            'content': d['content'],
            'tokens': toks
        })
    
    inv_pos = build_inverted_index_positional(docs_pos)
    
    docs = []
    for d in raw_data:
        toks = preprocess_text_basic(d['content'])
        toks = remove_punc_and_digits(toks)
        docs.append({
            'id': d['id'],
            'tokens': toks
        })
    
    freq_dict = build_global_frequency_dict(docs)
    docs = remove_top_frequent_words(docs, freq_dict, 50)
    docs = apply_stemming_lemmatizing(docs)
    tfidf_index = build_tfidf_index(docs, len(docs))
    
    dictionary_size = len(tfidf_index)
    postings_size = get_inverted_index_memory_size(inv_pos)
    print("Dictionary size (unique tokens):", dictionary_size)
    print("Postings lists size (bytes):", postings_size)
    
    print("ready")
    while True:
        q = input("query: ")
        if q.strip().lower() == "exit":
            break
        results = rank_documents(q, docs, tfidf_index)
        for idx in range(min(5, len(results))):
            doc_id, score = results[idx]
            print(doc_id, score)
            doc_info = next((x for x in docs_pos if x['id'] == doc_id), None)
            if doc_info:
                print("  ", doc_info['content'][:200], "...")
        print("-------")
