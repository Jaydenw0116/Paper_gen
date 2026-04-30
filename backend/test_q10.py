import sys
import zipfile
import re
sys.path.insert(0, '/Users/wuhuangjian/Desktop/Paper_gen/backend')

from app.core.xml_parser import QuestionParser

with open('../4C 10 test sol.docx', 'rb') as f:
    doc_bytes = f.read()

answers = QuestionParser.parse_document(doc_bytes)
print(f"解析出 {len(answers)} 个问题")

# 检查题号10的内容
for ans in answers:
    if ans.get('number') == '10.':
        print(f"找到题号10: {ans}")
        break
else:
    print("没有找到题号10")
    
# 检查第10个问题块的位置
print("\n检查答案文档中题号10附近的内容：")
with zipfile.ZipFile('../4C 10 test sol.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

lines = xml_content.split('<w:p')
for i in range(100, 115):
    if i < len(lines):
        part = lines[i]
        text_matches = re.findall(r'<w:t>([^<]+)</w:t>', part)
        if text_matches:
            full_text = ''.join(text_matches)
            if full_text.strip():
                print(f"段落 {i}: {repr(full_text)}")