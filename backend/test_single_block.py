import subprocess
import json
import zipfile
import re

# Upload
upload_result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../4C 10 test.docx',
     '-F', 'answer_file=@../4C 10 test sol.docx'],
    capture_output=True, text=True
)
upload_data = json.loads(upload_result.stdout)
session_id = upload_data['session_id']
first_q_id = upload_data['questions'][0]['id']
print(f"第一个问题ID: {first_q_id}")

# Download first answer block
subprocess.run([
    'curl', '-s', '-o', '/tmp/first_answer.docx',
    f"http://localhost:8000/api/download-question/{session_id}/{first_q_id}"
])

# Check content
try:
    with zipfile.ZipFile('/tmp/first_answer.docx', 'r') as z:
        xml_content = z.read('word/document.xml').decode('utf-8')
    
    matches = re.findall(r'<w:t>([^<]+)</w:t>', xml_content)
    print("\n第一个答案块的文本内容:")
    for m in matches[:20]:
        print(f"  {repr(m)}")
    
    number_like = [m for m in matches if re.match(r'^\s*\d+[\.．、]', m)]
    print(f"\n看起来像题号的内容: {number_like}")
    
except Exception as e:
    print(f"错误: {e}")
    with open('/tmp/first_answer.docx', 'rb') as f:
        content = f.read()
        print(f"文件内容前50字节: {content[:50]}")
