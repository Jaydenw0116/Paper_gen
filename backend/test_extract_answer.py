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
session_id = upload_data['session_id']

# 下载第一个问题的答案
question_id = upload_data['questions'][0]['id']
subprocess.run([
    'curl', '-s', f"http://localhost:8000/api/download-question/{session_id}/{question_id}",
    '-o', '/tmp/q1.docx'
])

# 检查第一个问题块的内容
with zipfile.ZipFile('/tmp/q1.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

matches = re.findall(r'<w:t>([^<]+)</w:t>', xml_content)
print("第一个问题块的文本内容:")
for m in matches[:30]:
    print(f"  {repr(m)}")

# 下载第三个问题的答案
question_id = upload_data['questions'][2]['id']
subprocess.run([
    'curl', '-s', f"http://localhost:8000/api/download-question/{session_id}/{question_id}",
    '-o', '/tmp/q3.docx'
])

with zipfile.ZipFile('/tmp/q3.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

matches = re.findall(r'<w:t>([^<]+)</w:t>', xml_content)
print("\n第三个问题块的文本内容:")
for m in matches[:30]:
    print(f"  {repr(m)}")
