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
question_ids = [q['id'] for q in upload_data['questions']]

# Upload to bank
subprocess.run([
    'curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload-to-bank',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps({'session_id': upload_data['session_id'], 'question_ids': question_ids})
])

# Compose
compose_result = subprocess.run([
    'curl', '-s', '-X', 'POST', 'http://localhost:8000/api/compose',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps({'question_ids': question_ids})
], capture_output=True, text=True)
compose_data = json.loads(compose_result.stdout)
compose_session_id = compose_data['session_id']

# Download answer
subprocess.run([
    'curl', '-s', '-o', '/tmp/test_answer_final.docx',
    f"http://localhost:8000/api/download/{compose_session_id}/answer"
])

# Check content
with zipfile.ZipFile('/tmp/test_answer_final.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# Count paragraphs
paragraphs = re.findall(r'<w:p[^>]*>', xml_content)
print(f"段落数: {len(paragraphs)}")

# Extract all text
matches = re.findall(r'<w:t>([^<]+)</w:t>', xml_content)
print(f"\n所有文本内容（前50个）:")
for i, m in enumerate(matches[:50]):
    print(f"{i+1}: {repr(m)}")

# Find number-like content
print("\n看起来像题号的内容:")
for m in matches:
    if re.match(r'^\s*\d+[\.．、]', m):
        print(f"  {repr(m)}")
