# weights_uni = tfidf_index.get("دانشگاه", {})
# sorted_weights = sorted(weights_uni.items(), key=lambda x: x[1], reverse=True)
# if sorted_weights:
#     highest_doc, highest_w = sorted_weights[0]
#     lowest_doc, lowest_w = sorted_weights[-1]
#     print("بیشترین وزن در سند:", highest_doc, "=", highest_w)
#     print("کمترین وزن در سند:", lowest_doc, "=", lowest_w)

# inverted_index_pos = {
#    "دانشگاه": {
#       10: [3, 15, 20],
#       12: [1],
#       ...
#    },
#    ...
# }

"""
word = "دانشگاه"
posting_dict = inverted_index_pos.get(word, {})

# استخراج شناسه‌های سند و مرتب‌سازی آن‌ها
all_docs = sorted(posting_dict.keys())

# ده سند اول
first_10_docs = all_docs[:10]

# گزارش موقعیت کلمه در هر سند
for doc_id in first_10_docs:
    positions = posting_dict[doc_id]
    print(f"سند {doc_id}: موقعیت‌ها = {positions}")
"""

# posting_dict = inverted_index_pos.get("دانشگاه", {})
# if posting_dict:
#     first_doc_id = min(posting_dict.keys())  # یا max() بسته به تعریف
#     positions = posting_dict[first_doc_id]
#     print("موقعیت در سند", first_doc_id, "=", positions)

# champion_lists["دانشگاه"] = [(doc_id1, weight1), (doc_id2, weight2), ...]

# if "دانشگاه" in champion_lists:
#     top_20 = champion_lists["دانشگاه"][:20]
#     for (doc, w) in top_20:
#         print("سند:", doc, "وزن:", w)

"""
items = list(tfidf_index["دانشگاه"].items())  # [(doc_id, weight), ...]
items.sort(key=lambda x: x[1], reverse=True)
champion_list_uni = items[:20]  # 20 سند اول

"""