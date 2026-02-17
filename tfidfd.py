def get_doc_tfidf_scores(doc_id, docs, tfidf_index):
    target_doc = next((d for d in docs if d['id'] == doc_id), None)
    if not target_doc:
        print(f"سندی با شناسه {doc_id} پیدا نشد.")
        return []
    
    tokens = target_doc['tokens']
    
    scores = []
    for token in set(tokens):
        tfidf_val = 0
        if token in tfidf_index and doc_id in tfidf_index[token]:
            tfidf_val = tfidf_index[token][doc_id]
        scores.append((token, tfidf_val))
    
    # مرتب‌سازی نزولی
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
