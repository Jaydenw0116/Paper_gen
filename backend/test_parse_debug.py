import sys
sys.path.insert(0, '/Users/wuhuangjian/Desktop/Paper_gen/backend')

from io import BytesIO
from docx import Document
from app.core.xml_parser import QuestionParser

# 读取试卷文档
with open('../OSM_ChapterTest_4B08_Lite_c.docx', 'rb') as f:
    doc_bytes = f.read()

# 解析文档
questions = QuestionParser.parse_document(doc_bytes)
print(f"解析出 {len(questions)} 个问题")

# 打印每个问题的详细信息
for i, q in enumerate(questions):
    print(f"\n问题 {i+1}:")
    print(f"  题号: {repr(q.get('number'))}")
    print(f"  起始索引: {q.get('start')}")
    print(f"  结束索引: {q.get('end')}")
    text = q.get('text', '')
    lines = text.split('\n')
    print(f"  文本行数: {len(lines)}")
    print(f"  前3行预览:")
    for j, line in enumerate(lines[:3]):
        print(f"    {j+1}: {repr(line[:100])}")
    
    # 检查第二题是否包含题号3
    if i == 1:  # 第二题（索引1）
        if '3.' in text:
            print("\n    ⚠️ 第二题包含题号3！")
            # 找到题号3的位置
            idx = text.find('3.')
            print(f"    题号3在第 {text[:idx].count('\\n') + 1} 行")
            # 显示题号3附近的内容
            print(f"    题号3附近内容: {repr(text[idx-20:idx+50])}")