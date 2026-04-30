import sys
sys.path.insert(0, '/Users/wuhuangjian/Desktop/Paper_gen/backend')

import subprocess
import json
import zipfile
import re

# 上传文件
result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../OSM_ChapterTest_4B08_Lite_c.docx',
     '-F', 'answer_file=@../OSM_ChapterTest_4B08_Lite_sol_c.docx'],
    capture_output=True, text=True
)
upload_data = json.loads(result.stdout)
question_ids = [q['id'] for q in upload_data['questions']]
session_id = upload_data['session_id']

print(f"上传成功，共 {len(question_ids)} 个问题")

# 上传到题库
upload_to_bank_data = json.dumps({'session_id': session_id, 'question_ids': question_ids})
subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload-to-bank',
     '-H', 'Content-Type: application/json',
     '-d', upload_to_bank_data],
    capture_output=True, text=True
)

# 使用原始顺序组卷（不打乱）
compose_data = json.dumps({'question_ids': question_ids})
result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/compose',
     '-H', 'Content-Type: application/json',
     '-d', compose_data],
    capture_output=True, text=True
)
compose_result = json.loads(result.stdout)
compose_session_id = compose_result['session_id']

# 下载生成的试卷
subprocess.run(['curl', '-s', '-o', '../generated_paper.docx',
                f'http://localhost:8000/api/download/{compose_session_id}/paper'])

# 检查试卷中的题号
print("\n=== 检查生成的试卷文件 ===")
with zipfile.ZipFile('../generated_paper.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# 提取所有题号
paper_numbers = []
for match in re.finditer(r'<w:t>(\d+[\.．、])</w:t>', xml_content):
    paper_numbers.append(match.group(1))

print(f"所有题号出现: {paper_numbers}")

# 统计每个题号出现的次数
from collections import Counter
counts = Counter(paper_numbers)
print(f"题号统计: {dict(counts)}")

# 检查是否有连续的题号
unique_numbers = []
seen = set()
for num in paper_numbers:
    if num not in seen:
        seen.add(num)
        unique_numbers.append(num)

print(f"去重后的题号: {unique_numbers}")

# 检查是否连续
for i in range(len(unique_numbers)):
    expected = f"{i+1}."
    if unique_numbers[i] != expected:
        print(f"发现不连续: 位置 {i+1}, 期望 {expected}, 实际 {unique_numbers[i]}")
        break
else:
    print("✓ 题号连续")