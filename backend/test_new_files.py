import sys
import os
sys.path.insert(0, '/Users/wuhuangjian/Desktop/Paper_gen/backend')

import requests
import json
import zipfile
import re

# 上传文件
print("=== 上传试卷和答案文件 ===")
question_file = '../OSM_ChapterTest_4B08_Lite_c.docx'
answer_file = '../OSM_ChapterTest_4B08_Lite_sol_c.docx'

with open(question_file, 'rb') as qf, open(answer_file, 'rb') as af:
    response = requests.post('http://localhost:8000/api/upload',
                            files={'question_file': qf, 'answer_file': af})

result = response.json()
print(f"上传结果: {result}")
session_id = result['session_id']
question_count = len(result['questions'])
print(f"解析出 {question_count} 个问题")

# 打印原始题号
print("\n=== 原始题号顺序 ===")
for q in result['questions']:
    print(f"  {q['original_no']}: {q['preview_text'][:30]}...")

# 打乱题目顺序
print("\n=== 打乱题目顺序 ===")
import random
shuffled_indices = list(range(question_count))
random.shuffle(shuffled_indices)
print(f"打乱后的索引: {shuffled_indices}")

# 创建打乱后的题目列表
questions_to_compose = []
for idx in shuffled_indices:
    q = result['questions'][idx]
    questions_to_compose.append({
        'id': q['id'],
        'order': len(questions_to_compose) + 1
    })

# 组卷生成
print("\n=== 组卷生成 ===")
compose_response = requests.post('http://localhost:8000/api/compose',
                                json={'session_id': session_id, 'questions': questions_to_compose})

compose_result = compose_response.json()
print(f"组卷结果: {compose_result}")

# 下载生成的试卷和答案
print("\n=== 下载生成的文件 ===")
paper_response = requests.get(f'http://localhost:8000/api/download-paper/{compose_result["paper_id"]}')
answer_response = requests.get(f'http://localhost:8000/api/download-answer/{compose_result["paper_id"]}')

# 保存文件
paper_path = '../generated_paper.docx'
answer_path = '../generated_answer.docx'

with open(paper_path, 'wb') as f:
    f.write(paper_response.content)
with open(answer_path, 'wb') as f:
    f.write(answer_response.content)

print(f"试卷保存到: {paper_path}")
print(f"答案保存到: {answer_path}")

# 检查生成的文件
print("\n=== 检查生成的试卷文件 ===")
with zipfile.ZipFile(paper_path, 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# 提取题号
paper_numbers = []
for match in re.finditer(r'<w:t>(\d+[\.．、])</w:t>', xml_content):
    paper_numbers.append(match.group(1))

# 去重并按出现顺序排列
unique_paper_numbers = []
seen = set()
for num in paper_numbers:
    if num not in seen:
        seen.add(num)
        unique_paper_numbers.append(num)

print(f"试卷题号: {unique_paper_numbers}")

# 检查是否连续
is_continuous = True
for i in range(len(unique_paper_numbers)):
    expected = f"{i+1}."
    if unique_paper_numbers[i] != expected:
        is_continuous = False
        print(f"  发现不连续: 期望 {expected}, 实际 {unique_paper_numbers[i]}")
        break

if is_continuous:
    print("  ✓ 试卷题号连续")

print("\n=== 检查生成的答案文件 ===")
with zipfile.ZipFile(answer_path, 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# 提取题号
answer_numbers = []
for match in re.finditer(r'<w:t>(\d+[\.．、])</w:t>', xml_content):
    answer_numbers.append(match.group(1))

# 去重并按出现顺序排列
unique_answer_numbers = []
seen = set()
for num in answer_numbers:
    if num not in seen:
        seen.add(num)
        unique_answer_numbers.append(num)

print(f"答案题号: {unique_answer_numbers}")

# 检查是否连续
is_continuous = True
for i in range(len(unique_answer_numbers)):
    expected = f"{i+1}."
    if unique_answer_numbers[i] != expected:
        is_continuous = False
        print(f"  发现不连续: 期望 {expected}, 实际 {unique_answer_numbers[i]}")
        break

if is_continuous:
    print("  ✓ 答案题号连续")

# 检查试卷和答案题号是否一致
if unique_paper_numbers == unique_answer_numbers:
    print("\n✓ 试卷和答案题号一致")
else:
    print("\n✗ 试卷和答案题号不一致")
    print(f"  试卷题号: {unique_paper_numbers}")
    print(f"  答案题号: {unique_answer_numbers}")