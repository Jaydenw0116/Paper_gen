import sys
sys.path.insert(0, '/Users/wuhuangjian/Desktop/Paper_gen/backend')

import json
from io import BytesIO
from app.core.xml_parser import QuestionParser

# 读取答案文档
with open('../4C 10 test sol.docx', 'rb') as f:
    doc_bytes = f.read()

# 解析答案文档
answers = QuestionParser.parse_document(doc_bytes)
print(f"答案文档解析出 {len(answers)} 个问题")

for i, ans in enumerate(answers):
    print(f"\n答案 {i+1}:")
    print(f"  题号: {repr(ans.get('number'))}")
    print(f"  起始索引: {ans.get('start')}")
    print(f"  结束索引: {ans.get('end')}")
    text = ans.get('text', '')
    print(f"  文本长度: {len(text)}")
    print(f"  预览: {repr(text[:100])}")