import zipfile
import re
from io import BytesIO
from docx import Document
from app.core.xml_parser import QuestionParser

with open('../4C 10 test sol.docx', 'rb') as f:
    doc_bytes = f.read()

answers = QuestionParser.parse_document(doc_bytes)
print(f"答案文档解析出 {len(answers)} 个问题")

for i, ans in enumerate(answers):
    print(f"\n答案 {i+1}:")
    print(f"  题号: {repr(ans.get('number'))}")
    print(f"  预览: {repr(ans.get('text', '')[:80])}")