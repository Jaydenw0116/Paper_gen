import sys
import json
import subprocess
import zipfile
import re

# Upload files
upload_result = subprocess.run(
    ['curl', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../4C 10 test.docx',
     '-F', 'answer_file=@../4C 10 test sol.docx'],
    capture_output=True, text=True
)

upload_data = json.loads(upload_result.stdout)
print(f"上传了 {len(upload_data['questions'])} 个问题")

# 检查每个问题的原始题号
for i, q in enumerate(upload_data['questions']):
    print(f"{i+1}. 原始题号: {q['original_no']}, 预览: {q['preview_text'][:50]}...")

# 检查答案文档中的题号
with zipfile.ZipFile('../4C 10 test sol.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# 找出所有看起来像题号的内容
matches = re.findall(r'<w:t>([^<]+)</w:t>', xml_content)
number_like = [(m, i) for i, m in enumerate(matches) if re.match(r'^\s*\d+[\.．、]', m)]
print("\n答案文档中看起来像题号的内容:")
for num, idx in number_like[:20]:
    print(f"  {repr(num)}")
