import json

def add_new_document(json_path, doc_id_str, doc_text):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data[doc_id_str] = {"content": doc_text}
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

add_new_document(
    json_path="data/news.json", 
    doc_id_str="75", 
    doc_text="این یک خبر جدید است که می‌خواهیم به مجموعه اسناد اضافه کنیم."
)