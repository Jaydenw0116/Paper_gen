import sys
sys.path.insert(0, '/Users/wuhuangjian/Desktop/Paper_gen/backend')

import re
from io import BytesIO
from docx import Document
from app.core.xml_parser import QuestionParser

# 测试正则表达式
test_cases = ['1.', '10.', '10', '10A', 'A.', '  3.']
print("测试正则表达式匹配：")
for tc in test_cases:
    match = QuestionParser.QUESTION_NUMBER_REGEX.match(tc)
    print(f"  '{tc}' -> {match.group() if match else None}")

# 测试只有题号的情况
print("\n测试验证逻辑：")
question = {
    'number': '10.',
    'text': '10.'
}
text = question.get('text', '')
lines = text.split('\n')
first_line = lines[0].strip()
print(f"文本: {repr(text)}")
print(f"行数: {len(lines)}")
print(f"第一行: {repr(first_line)}")

number_match = QuestionParser.QUESTION_NUMBER_REGEX.match(first_line)
if number_match:
    first_line_content = first_line[len(number_match.group()):].strip()
    print(f"去掉题号后的内容: {repr(first_line_content)}")
    print(f"内容长度: {len(first_line_content)}")
    if len(first_line_content) < 3 and len(lines) <= 2:
        if len(lines) == 1 and first_line_content == '':
            print("-> 保留（单一行且只有题号）")
        else:
            print("-> 跳过")
    else:
        print("-> 保留")
else:
    print("-> 没有匹配到题号")